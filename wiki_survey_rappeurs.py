import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Classement Rap Optimisé", layout="centered")
st.title("⚡ Classe ton top 20 de rappeurs (duels optimisés)")

rappers = [
    "Booba", "Ninho", "Alpha Wann", "Nekfeu", "Damso", "La Fêve", "Zamdane", "Caballero",
    "Khali", "Laylow", "SCH", "Theodora", "Mairo", "Hamza", "Yvnnis", "NeS", "Luther",
    "Bekar", "Karmen", "H Jeunecrack"
]

# Fonction de tri personnalisé avec fusion (merge sort)
def merge_sort_duel(array):
    if len(array) <= 1:
        return array
    mid = len(array) // 2
    left = merge_sort_duel(array[:mid])
    right = merge_sort_duel(array[mid:])
    return merge(left, right)

# Merge avec intervention utilisateur
def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        st.markdown(f"### Qui préfères-tu ?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(left[i], key=f"{left[i]} vs {right[j]} - L"):
                st.session_state.duel_result.append((left[i], right[j]))
                result.append(left[i])
                i += 1
                st.rerun()
        with col2:
            if st.button(right[j], key=f"{left[i]} vs {right[j]} - R"):
                st.session_state.duel_result.append((right[j], left[i]))
                result.append(right[j])
                j += 1
                st.rerun()
        st.stop()  # attendre la réponse avant de continuer

    result += left[i:]
    result += right[j:]
    return result

# Initialisation
if "sorted_list" not in st.session_state:
    st.session_state.duel_result = []
    st.session_state.sorted_list = merge_sort_duel(random.sample(rappers, len(rappers)))

# Classement final
if len(st.session_state.duel_result) >= len(rappers) * int((len(rappers)).bit_length()):
    st.success("Classement complété avec succès !")
    final_ranking = st.session_state.sorted_list
    df = pd.DataFrame({"Rang": list(range(1, len(final_ranking)+1)), "Rappeur": final_ranking})
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Télécharger en CSV", df.to_csv(index=False), file_name="classement_rappeurs.csv")

    if st.button("🔁 Recommencer"):
        for key in ["sorted_list", "duel_result"]:
            del st.session_state[key]
        st.rerun()
