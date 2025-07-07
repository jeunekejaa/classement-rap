import streamlit as st
import random
import pandas as pd
import math

# Configuration de la page
st.set_page_config(page_title="Classement Rap Optimisé", layout="centered")
st.title("⚡ Classe ton top 20 de rappeurs (duels optimisés)")

# Liste des rappeurs
rappers = [
    "Booba", "Ninho", "Alpha Wann", "Nekfeu", "Damso",
    "La Fêve", "Zamdane", "Caballero", "Khali", "Laylow",
    "SCH", "Theodora", "Mairo", "Hamza", "Yvnnis",
    "NeS", "Luther", "Bekar", "Karmen", "H Jeunecrack"
]

# Nombre optimal de duels (~ n·log₂(n))
total_needed = math.ceil(len(rappers) * math.log2(len(rappers)))

# Fonction de tri personnalisé (merge sort interatif)
def merge_sort_duel(array):
    if len(array) <= 1:
        return array
    mid = len(array) // 2
    left = merge_sort_duel(array[:mid])
    right = merge_sort_duel(array[mid:])
    return merge(left, right)

# Fusion interactive
def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        st.markdown("### Qui préfères-tu ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(left[i], key=f"L{left[i]}_{right[j]}"):
                st.session_state.duel_result.append((left[i], right[j]))
                result.append(left[i]); i += 1; st.rerun()
        with col2:
            if st.button(right[j], key=f"R{left[i]}_{right[j]}"):
                st.session_state.duel_result.append((right[j], left[i]))
                result.append(right[j]); j += 1; st.rerun()
        st.stop()
    result += left[i:]
    result += right[j:]
    return result

# Initialisation de l'état
if 'sorted_list' not in st.session_state:
    shuffled = random.sample(rappers, len(rappers))
    st.session_state.duel_result = []
    st.session_state.sorted_list = merge_sort_duel(shuffled)

# Progression
done = len(st.session_state.duel_result)
progress = int(100 * min(done, total_needed) / total_needed)

# Choix de montrer le classement
show = st.checkbox("Afficher classement", value=False)
if show:
    st.markdown(f"**Progression : {progress}%**")
    st.progress(progress)
    if done < total_needed:
        st.info("🔍 Classement en construction – plus tu votes, plus il sera précis.")
    else:
        st.success("✅ Classement complet et fiable !")
    # Affichage du classement (sans colonne Rang)
    df = pd.DataFrame({"Rappeur": st.session_state.sorted_list})
    st.dataframe(df, use_container_width=True)
    if done >= total_needed:
        st.download_button("📥 Télécharger en CSV", df.to_csv(index=False), file_name="classement_rappeurs.csv")

# Message final et bouton recommencer
if done >= total_needed and not st.session_state.get('restarted', False):
    st.success("🎉 Tu as complété tous les duels nécessaires !")
    if st.button("🔁 Recommencer"):
        for k in ['sorted_list','duel_result']:
            del st.session_state[k]
        st.session_state.restarted = True
        st.rerun()
