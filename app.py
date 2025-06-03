import streamlit as st
from corrector import correct_french
from qa_model import load_french_llm, answer_question

st.title("🇫🇷 FrançaisQA — Outil de correction et de réponse en français")

tab1, tab2 = st.tabs(["📝 Correction de texte", "❓ Questions / Réponses"])

with tab1:
    text_input = st.text_area("Entrez votre phrase en français:")
    if st.button("Corriger"):
        corrected, explanations = correct_french(text_input)
        st.success(f"✅ Phrase corrigée : {corrected}")
        st.markdown("#### ✏️ Explications :")
        for exp in explanations:
            st.write(f"- **Erreur**: `{exp['error']}` → **Message**: {exp['message']}")
            st.write(f"  **Suggestions**: {', '.join(exp['suggestions'])}")

with tab2:
    st.markdown("Posez une question en français.")
    user_question = st.text_input("Votre question:")
    if st.button("Répondre"):
        st.write("⏳ Génération de la réponse...")
        pipe = load_french_llm()
        answer = answer_question(pipe, user_question)
        st.success(f"💬 Réponse : {answer}")

