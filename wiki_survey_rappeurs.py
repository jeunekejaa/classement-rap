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
    return [left, right]  # ne fusionne pas tout de suite

# Initialisation
if "stack" not in st.session_state:
    shuffled = random.sample(rappers, len(rappers))
    st.session_state.stack = [merge_sort_duel(shuffled)]
    st.session_state.results = []
    st.session_state.duel_result = []

# Fonction de fusion interactive
def step_merge():
    stack = st.session_state.stack
    results = st.session_state.results

    while stack:
        top = stack[-1]

        # Si sous-liste fusionnable
        if isinstance(top, list) and len(top) == 2 and all(isinstance(x, list) == False for x in top):
            left, right = top
            if not left:
                stack.pop()
                results.append(right)
            elif not right:
                stack.pop()
                results.append(left)
            else:
                a, b = left[0], right[0]
                st.markdown("### Qui préfères-tu ?")
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(a):
                        st.session_state.duel_result.append((a, b))
                        stack[-1][0] = left[1:]
                        stack[-1][1] = right
                        results.append([a])
                        st.rerun()
                with col2:
                    if st.button(b):
                        st.session_state.duel_result.append((b, a))
                        stack[-1][0] = left
                        stack[-1][1] = right[1:]
                        results.append([b])
                        st.rerun()
                return  # afficher un duel 
        elif isinstance(top, list):
            # Fusionner les deux dernières sous-listes si possible
            if len(top) == 2 and all(isinstance(x, list) for x in top):
                stack.pop()
                stack.append(top[0] + top[1])
            else:
                break
        else:
            stack.pop()
            results.append(top)

    if not stack and len(results) == 1:
        st.session_state.sorted_list = results[0]

# Appel de fusion
step_merge()

# Calcul du classement
total_needed = len(rappers) * int((len(rappers)).bit_length())
done = len(st.session_state.duel_result)
progress = int(100 * done / total_needed)

# Bouton de consultation dynamique
button_label = "📊 Consulter votre classement actuel"
if done >= total_needed:
    button_label = "✅ Classement complet"

if st.button(button_label):
    st.markdown(f"### Progression : {progress}%")
    st.progress(progress)

    if done >= total_needed:
        st.success("✅ Tu as atteint le nombre minimal de duels pour un classement fiable.")
    else:
        st.info("🔍 Ce classement est en construction. En continuant, tu amélioreras sa précision.")

    if "sorted_list" in st.session_state:
        classement_actuel = st.session_state.sorted_list
        df_live = pd.DataFrame({"Rang": list(range(1, len(classement_actuel)+1)), "Rappeur": classement_actuel})
        st.dataframe(df_live, use_container_width=True)

# Classement final
if done >= total_needed and "sorted_list" in st.session_state:
    st.success("Tu as complété suffisamment de duels pour produire un classement fiable !")
    final_ranking = st.session_state.sorted_list
    df = pd.DataFrame({"Rang": list(range(1, len(final_ranking)+1)), "Rappeur": final_ranking})
    st.dataframe(df, use_container_width=True)
    st.download_button("📥 Télécharger en CSV", df.to_csv(index=False), file_name="classement_rappeurs.csv")

    if st.button("🔁 Recommencer"):
        for key in ["sorted_list", "duel_result", "stack", "results"]:
            del st.session_state[key]
        st.rerun()
