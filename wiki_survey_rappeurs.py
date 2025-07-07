import streamlit as st
import random
import itertools
import pandas as pd

st.set_page_config(page_title="Classement Rap", layout="centered")
st.title("🎤 Classe ton top 20 de rappeurs francophones")

# Liste des rappeurs
rappers = [
    "Booba", "Ninho", "Alpha Wann", "Nekfeu", "Damso", "La Fêve", "Zamdane", "Caballero",
    "Khali", "Laylow", "SCH", "Theodora", "Mairo", "Hamza", "Yvnnis", "NeS", "Luther",
    "Bekar", "Karmen", "H Jeunecrack"
]

# Initialiser session state
if "pairs" not in st.session_state:
    st.session_state.pairs = list(itertools.combinations(rappers, 2))
    random.shuffle(st.session_state.pairs)
    st.session_state.index = 0
    st.session_state.scores = {rapper: 0 for rapper in rappers}

# Affichage des duels
if st.session_state.index < len(st.session_state.pairs):
    a, b = st.session_state.pairs[st.session_state.index]
    st.markdown(f"## Duel {st.session_state.index + 1} / {len(st.session_state.pairs)}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(a):
            st.session_state.scores[a] += 1
            st.session_state.index += 1
            st.experimental_rerun()
    with col2:
        if st.button(b):
            st.session_state.scores[b] += 1
            st.session_state.index += 1
            st.experimental_rerun()
else:
    # Résultats finaux
    st.success("Tu as complété tous les duels ! Voici ton classement :")
    sorted_scores = sorted(st.session_state.scores.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(sorted_scores, columns=["Rappeur", "Score"])
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Télécharger le classement en CSV", df.to_csv(index=False), file_name="classement_rappeurs.csv")

    if st.button("🔁 Recommencer"):
        for key in ["pairs", "index", "scores"]:
            del st.session_state[key]
        st.experimental_rerun()
