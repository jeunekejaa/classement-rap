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

# Fonction de tri personnalisé (merge sort interactif)
def merge_sort_duel(array):
    if len(array) <= 1:
        return array
    mid = len(array) // 2
    left = merge_sort_duel(array[:mid])
    right = merge_sort_duel(array[mid:])
    return left, right

# Initialisation de l'état
if 'duel_result' not in st.session_state or 'stack' not in st.session_state:
    shuffled = random.sample(rappers, len(rappers))
    # stack contient soit tuple (left, right) à fusionner, soit sorted segments
    st.session_state.stack = [merge_sort_duel(shuffled)]
    st.session_state.duel_result = []
    st.session_state.sorted = False

# Affichage du checkbox pour consulter le classement
display = st.checkbox("Afficher classement", value=False)
# Calcul de la progression
done = len(st.session_state.duel_result)
progress = int(100 * min(done, total_needed) / total_needed)

# Si on souhaite afficher le classement
if display:
    st.markdown(f"**Progression : {progress}%**")
    st.progress(progress)
    if done < total_needed:
        st.info("🔍 Classement en construction – plus tu votes, plus il sera précis.")
    else:
        st.success("✅ Classement complet et fiable !")
    df = pd.DataFrame({"Rappeur": st.session_state.get('sorted_list', [])})
    st.dataframe(df, use_container_width=True)
    if done >= total_needed:
        st.download_button("📥 Télécharger en CSV", df.to_csv(index=False), file_name="classement_rappeurs.csv")

# Si pas déjà trié et qu'on ne regarde pas seulement le classement, on lance un duel
if not st.session_state.sorted and not display:
    # extraire un élément à fusionner
    left, right = st.session_state.stack.pop(0)
    # garantir que left/right sont listes
    left = left if isinstance(left, list) else [left]
    right = right if isinstance(right, list) else [right]
    # fusion interactive
    i = j = 0
    result = []
    while i < len(left) and j < len(right):
        st.markdown("### Qui préfères-tu ?")
        col1, col2 = st.columns(2)
        a, b = left[i], right[j]
        with col1:
            if st.button(a, key=f"L{a}_{b}"):
                st.session_state.duel_result.append((a,b))
                result.append(a); i+=1; st.experimental_rerun()
        with col2:
            if st.button(b, key=f"R{a}_{b}"):
                st.session_state.duel_result.append((b,a))
                result.append(b); j+=1; st.experimental_rerun()
        return
    result += left[i:] + right[j:]
    # ajouter segment fusionné et continuer
    st.session_state.stack.append(result)
    # si il ne reste plus qu'un segment, le tri est fait
    if len(st.session_state.stack)==1 and not any(isinstance(x, tuple) for x in st.session_state.stack):
        st.session_state.sorted_list = st.session_state.stack[0]
        st.session_state.sorted = True

# Message final et bouton recommencer
if st.session_state.get('sorted', False):
    st.success("🎉 Tri terminé !")
    if st.button("🔁 Recommencer"):
        for k in ['duel_result','stack','sorted','sorted_list']:
            if k in st.session_state: del st.session_state[k]
        st.experimental_rerun()
