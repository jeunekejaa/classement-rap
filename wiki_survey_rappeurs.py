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

# Nombre de comparaisons optimales (approx. n·log₂(n))
total_needed = math.ceil(len(rappers) * math.log2(len(rappers)))

# Initialisation de l'état
if 'sorted_list' not in st.session_state:
    shuffled = random.sample(rappers, len(rappers))
    st.session_state.sorted_list = [shuffled.pop(0)]  # première liste triée
    st.session_state.remaining = shuffled           # reste à insérer
    st.session_state.current = None
    st.session_state.low = 0
    st.session_state.high = 0
    st.session_state.inserting = False
    st.session_state.duel_count = 0

# Phase de duel pour insertion (tri par insertion binaire)
if st.session_state.remaining:
    # Démarre l'insertion d'un nouvel élément si nécessaire
    if not st.session_state.inserting:
        st.session_state.current = st.session_state.remaining.pop(0)
        st.session_state.low = 0
        st.session_state.high = len(st.session_state.sorted_list)
        st.session_state.inserting = True

    # Tant que l'élément n'est pas inséré
    if st.session_state.inserting:
        a = st.session_state.current
        low = st.session_state.low
        high = st.session_state.high
        mid = (low + high) // 2
        b = st.session_state.sorted_list[mid]

        st.markdown("### Qui préfères-tu ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(a, key="duel_a"):
                st.session_state.duel_count += 1
                # a > b → insérer avant b
                st.session_state.high = mid
                if st.session_state.low >= st.session_state.high:
                    pos = st.session_state.low
                    st.session_state.sorted_list.insert(pos, a)
                    st.session_state.inserting = False
                st.rerun()
        with col2:
            if st.button(b, key="duel_b"):
                st.session_state.duel_count += 1
                # b ≥ a → insérer après b
                st.session_state.low = mid + 1
                if st.session_state.low >= st.session_state.high:
                    pos = st.session_state.low
                    st.session_state.sorted_list.insert(pos, a)
                    st.session_state.inserting = False
                st.rerun()

# Calcul de la progression
done = st.session_state.duel_count
progress = int(100 * min(done, total_needed) / total_needed)

# Bouton de consultation toujours visible
button_label = "📊 Consulter votre classement actuel" if done < total_needed else "✅ Classement complet"
if st.button(button_label):
    st.markdown(f"### Progression : {progress}%")
    st.progress(progress)
    if done < total_needed:
        st.info("🔍 Classement en construction – plus tu votes, plus il sera précis.")
    else:
        st.success("🎉 Classement complet et fiable !")
    # Affichage du classement courant
    df_live = pd.DataFrame({
        "Rang": list(range(1, len(st.session_state.sorted_list) + 1)),
        "Rappeur": st.session_state.sorted_list
    })
    st.dataframe(df_live, use_container_width=True)
    # Téléchargement si terminé
    if done >= total_needed:
        st.download_button("📥 Télécharger en CSV", df_live.to_csv(index=False), file_name="classement_rappeurs.csv")

# Message final si terminé
if done >= total_needed and not st.session_state.inserting:
    st.success("✅ Tu as complété tous les duels nécessaires pour un classement fiable !")
    if st.button("🔁 Recommencer"):
        for key in ['sorted_list','remaining','current','low','high','inserting','duel_count']:
            del st.session_state[key]
        st.rerun()
