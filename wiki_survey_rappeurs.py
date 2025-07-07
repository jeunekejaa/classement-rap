import streamlit as st
import random
import pandas as pd
import math

# Config page
st.set_page_config(page_title="Classement Rap par Elo", layout="centered")
st.title("🏆 Classement Rap par Elo")

# Paramètres élévation
K = 32
threshold = st.sidebar.slider("Seuil de stabilité (points)", min_value=0.0, max_value=10.0, value=1.0, step=0.5)
st.sidebar.markdown("Le classement s'arrête quand la variation moyenne des 10 derniers duels < seuil.")

# Liste des rappeurs
rappers = [
    "Booba", "Ninho", "Alpha Wann", "Nekfeu", "Damso",
    "La Fêve", "Zamdane", "Caballero", "Khali", "Laylow",
    "SCH", "Theodora", "Mairo", "Hamza", "Yvnnis",
    "NeS", "Luther", "Bekar", "Karmen", "H Jeunecrack"
]

# Initialisation
if 'ratings' not in st.session_state:
    st.session_state.ratings = {r: 1500.0 for r in rappers}
    st.session_state.history = []
    st.session_state.stable = False
    st.session_state.duel = None

# Choix duel
if not st.session_state.stable:
    st.session_state.duel = random.sample(rappers, 2)

# Affichage duel
if not st.session_state.stable and st.session_state.duel:
    a, b = st.session_state.duel
    st.markdown(f"### Qui préfères-tu ?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button(a, key=f"win_{a}"):
            winner, loser = a, b
            st.rerun()
    with col2:
        if st.button(b, key=f"win_{b}"):
            winner, loser = b, a
            st.rerun()
    st.stop()

# Mise à jour Elo
if 'winner' in locals():
    Ra = st.session_state.ratings[winner]
    Rb = st.session_state.ratings[loser]
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 - Ea
    delta_a = K * (1 - Ea)
    delta_b = K * (0 - Eb)
    st.session_state.ratings[winner] += delta_a
    st.session_state.ratings[loser] += delta_b
    change = abs(delta_a) + abs(delta_b)
    st.session_state.history.append(change)
    # Check stabilité
    if len(st.session_state.history) >= 10:
        avg_change = sum(st.session_state.history[-10:]) / 10
        if avg_change < threshold:
            st.session_state.stable = True
    # Reset duel
    del winner, loser

# Affichage progression et statut
if st.session_state.stable:
    st.success("✅ Classement stable atteint !")
else:
    if st.session_state.history:
        last_changes = st.session_state.history[-10:]
        avg = sum(last_changes) / len(last_changes)
        st.info(f"Variation moyenne (10 derniers duels) : {avg:.2f} points")

# Afficher classement
if st.checkbox("Afficher classement", value=True):
    ranked = sorted(st.session_state.ratings.items(), key=lambda x: x[1], reverse=True)
    df = pd.DataFrame(ranked, columns=["Rappeur", "Elo"])
    st.dataframe(df, use_container_width=True)
    if st.session_state.stable:
        st.download_button("📥 Télécharger CSV", df.to_csv(index=False), file_name="classement_rappeurs_elo.csv")

# Réinitialiser
if st.button("🔁 Réinitialiser"):
    for key in ['ratings', 'history', 'stable', 'duel']:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
