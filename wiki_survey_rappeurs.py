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

# Initialisation de l'état
if 'sorted_list' not in st.session_state:
    shuffled = random.sample(rappers, len(rappers))
    st.session_state.sorted_list = [shuffled.pop(0)]
    st.session_state.remaining = shuffled[:]  # éléments à insérer
    st.session_state.current = None
    st.session_state.low = 0
    st.session_state.high = 0
    st.session_state.inserting = False
    st.session_state.duel_count = 0

# Checkbox pour afficher le classement
display = st.checkbox("Afficher classement", value=False)
# Calcul de la progression
done = st.session_state.duel_count
progress = int(100 * min(done, total_needed) / total_needed)

# Affichage du classement si demandé
if display:
    st.markdown(f"**Progression : {progress}%**")
    st.progress(progress)
    if done < total_needed:
        st.info("🔍 Classement en construction – plus tu votes, plus il sera précis.")
    else:
        st.success("✅ Classement complet et fiable !")
    # Affichage du classement sans colonne Rang
    df = pd.DataFrame({"Rappeur": st.session_state.sorted_list})
    st.dataframe(df["Rappeur"], use_container_width=True)
    if done >= total_needed:
        st.download_button("📥 Télécharger en CSV", df.to_csv(index=False), file_name="classement_rappeurs.csv")

# Phase de duel pour insertion
if st.session_state.remaining:
    if not st.session_state.inserting:
        # Initialiser un nouvel élément à insérer
        st.session_state.current = st.session_state.remaining.pop(0)
        st.session_state.low = 0
        st.session_state.high = len(st.session_state.sorted_list)
        st.session_state.inserting = True

    if st.session_state.inserting:
        a = st.session_state.current
        low = st.session_state.low
        high = st.session_state.high
        mid = (low + high) // 2
        b = st.session_state.sorted_list[mid]

        st.markdown("### Qui préfères-tu ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(a, key=f"a_{a}_{b}"):
                st.session_state.duel_count += 1
                # a > b : insérer avant b
                st.session_state.high = mid
                if st.session_state.low >= st.session_state.high:
                    st.session_state.sorted_list.insert(st.session_state.low, a)
                    st.session_state.inserting = False
                st.rerun()
        with col2:
            if st.button(b, key=f"b_{a}_{b}"):
                st.session_state.duel_count += 1
                # b >= a : insérer après b
                st.session_state.low = mid + 1
                if st.session_state.low >= st.session_state.high:
                    st.session_state.sorted_list.insert(st.session_state.low, a)
                    st.session_state.inserting = False
                st.rerun()

# Message final et bouton recommencer
if not st.session_state.remaining and not st.session_state.inserting:
    st.success("🎉 Tri terminé !")
    if st.button("🔁 Recommencer"):
        for key in ['sorted_list', 'remaining', 'current', 'low', 'high', 'inserting', 'duel_count']:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()
