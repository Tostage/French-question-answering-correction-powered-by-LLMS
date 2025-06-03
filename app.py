import os
os.environ["TORCH_ALLOW_TF32_CUDA"] = "0"  # Optional torch fix if using GPU

import streamlit as st
from corrector import correct_french
from qa_model import load_french_llm, answer_question

st.set_page_config(page_title="FrançaisQA", page_icon="🇫🇷")

st.title("🇫🇷 FrançaisQA — Outil intelligent de correction et de réponse en français")

tab1, tab2 = st.tabs(["📝 Correction de texte", "❓ Questions / Réponses"])

# --- Grammar Correction Tab ---
with tab1:
    st.subheader("Corrigez votre phrase en français")
    text_input = st.text_area("✍️ Entrez votre phrase ici :", height=150)
    
    if st.button("Corriger"):
        if not text_input.strip():
            st.warning("Veuillez entrer une phrase à corriger.")
        else:
            corrected, explanations = correct_french(text_input)
            st.success(f"✅ Phrase corrigée :\n\n{corrected}")
            if explanations:
                st.markdown("#### ✏️ Explications :")
                for exp in explanations:
                    st.markdown(f"- **Erreur**: `{exp['error']}` → **Message**: {exp['message']}")
                    if exp["suggestions"]:
                        st.markdown(f"  - **Suggestions**: {', '.join(exp['suggestions'])}")
            else:
                st.info("Aucune erreur détectée.")

# --- Question Answering Tab ---
with tab2:
    st.subheader("Posez une question en français")
    user_question = st.text_input("❓ Votre question :")
    
    if st.button("Répondre"):
        if not user_question.strip():
            st.warning("Veuillez entrer une question.")
        else:
            with st.spinner("Génération de la réponse..."):
                pipe = load_french_llm()
                answer = answer_question(pipe, user_question)
                st.success(f"💬 Réponse : {answer}")
