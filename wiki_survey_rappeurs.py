import streamlit as st
import random
import pandas as pd
import math

# --- Configuration de la page ---
st.set_page_config(
    page_title="Rap Sorter",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("# 🎤 Rap Sorter — Classement par duels")
st.markdown("**Reproduit l’interface NHL Sorter pour tes rappeurs préférés!**")

# --- Liste des rappeurs ---
RAPPERS = [
    "Booba", "Ninho", "Alpha Wann", "Nekfeu", "Damso",
    "La Fêve", "Zamdane", "Caballero", "Khali", "Laylow",
    "SCH", "Theodora", "Mairo", "Hamza", "Yvnnis",
    "NeS", "Luther", "Bekar", "Karmen", "H Jeunecrack"
]

# --- Paramètres Elo ---
K_FACTOR = 32

# Sidebar: seuil de stabilité
threshold = st.sidebar.slider(
    "Seuil de stabilité (variation moyenne sur les 10 derniers duels)",
    min_value=0.0,
    max_value=20.0,
    value=1.0,
    step=0.5
)
st.sidebar.markdown(
    "Lorsque la variation moyenne des 10 derniers duels est < seuil, le classement est considéré comme stable."
)

# --- Initialisation de l'état ---
if "ratings" not in st.session_state:
    st.session_state.ratings = {r: 1500.0 for r in RAPPERS}
    st.session_state.history = []                 # variations pour la stabilité
    st.session_state.stable = False
    st.session_state.current_duel = None           # tuple (a, b)

# --- Sélection d'un duel aléatoire tant que non stable ---
if not st.session_state.stable:
    # Choisir deux rappeurs distincts
    a, b = random.sample(RAPPERS, 2)
    st.session_state.current_duel = (a, b)
else:
    st.session_state.current_duel = None

# --- Affichage du duel ---
if st.session_state.current_duel is not None:
    a, b = st.session_state.current_duel
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.markdown(f"### {a}")
        if st.button("👍", key=f"vote_{a}"):
            winner, loser = a, b
            st.session_state.process_vote = True
    with col2:
        st.markdown(f"### {b}")
        if st.button("👍", key=f"vote_{b}"):
            winner, loser = b, a
            st.session_state.process_vote = True

    # Stopper la rerun automatique
    if not st.session_state.get("process_vote", False):
        st.stop()

# --- Traitement du vote Elo ---
if st.session_state.get("process_vote", False):
    # Calcul des scores attendus
    Ra = st.session_state.ratings[winner]
    Rb = st.session_state.ratings[loser]
    Ea = 1 / (1 + 10 ** ((Rb - Ra) / 400))
    Eb = 1 - Ea
    # Mise à jour
    delta_a = K_FACTOR * (1 - Ea)
    delta_b = K_FACTOR * (0 - Eb)
    st.session_state.ratings[winner] += delta_a
    st.session_state.ratings[loser] += delta_b
    # Historique des variations
    st.session_state.history.append(abs(delta_a) + abs(delta_b))
    # Réinitialiser flag
    st.session_state.process_vote = False
    # Vérifier stabilité
    if len(st.session_state.history) >= 10:
        avg_change = sum(st.session_state.history[-10:]) / 10
        if avg_change < threshold:
            st.session_state.stable = True
    # Recharger la page
    st.experimental_rerun()

# --- Affichage de la progression et statut ---
st.markdown("---")
if st.session_state.history:
    last_changes = st.session_state.history[-10:]
    avg_change = sum(last_changes) / len(last_changes)
    st.info(f"**Variation moyenne (10 derniers duels)** : {avg_change:.2f} points")

if st.session_state.stable:
    st.success("✅ Classement stable atteint !")
else:
    st.warning("Choisis tes préférences jusqu'à stabilisation 🕹️")

# --- Affichage du classement ---
st.markdown("---")
st.header("📊 Classement en cours ou final")
ranked = sorted(
    st.session_state.ratings.items(),
    key=lambda x: x[1],
    reverse=True
)
df = pd.DataFrame(ranked, columns=["Rappeur", "Elo"])  # sans rang explicite
st.dataframe(df, use_container_width=True)

if st.session_state.stable:
    st.download_button(
        "📥 Télécharger le classement CSV",
        df.to_csv(index=False).encode('utf-8-sig'),
        file_name="classement_rappeurs_elo.csv",
        mime="text/csv"
    )

# --- Bouton réinitialiser ---
st.markdown("---")
if st.button("🔁 Réinitialiser le classement"):
    for key in ["ratings", "history", "stable", "current_duel"]:
        if key in st.session_state:
            del st.session_state[key]
    st.experimental_rerun()
