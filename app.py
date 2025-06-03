import os
os.environ["TORCH_ALLOW_TF32_CUDA"] = "0"  # Torch/Streamlit fix

import streamlit as st
from corrector import correct_french
from qa_model import load_french_llm, answer_question

st.set_page_config(page_title="FrançaisQA", page_icon="🇫🇷")
st.title("🇫🇷 FrançaisQA — Correction grammaticale et questions en français")

tab1, tab2 = st.tabs(["📝 Correction", "❓ Q&A"])

with tab1:
    text_input = st.text_area("Entrez une phrase en français :", height=150)
    if st.button("Corriger"):
        if not text_input.strip():
            st.warning("Veuillez entrer une phrase.")
        else:
            corrected, explanations = correct_french(text_input)
            st.success(f"✅ Correction :\n\n{corrected}")
            if explanations:
                st.markdown("#### ✏️ Explications :")
                for exp in explanations:
                    st.markdown(f"- **Erreur**: `{exp['error']}` → {exp['message']}")
                    if exp['suggestions']:
                        st.markdown(f"  - **Suggestions**: {', '.join(exp['suggestions'])}")
            else:
                st.info("Aucune erreur détectée.")

with tab2:
    user_question = st.text_input("Posez votre question :")
    if st.button("Répondre"):
        if not user_question.strip():
            st.warning("Veuillez poser une question.")
        else:
            with st.spinner("Génération de la réponse..."):
                pipe = load_french_llm()
                answer = answer_question(pipe, user_question)
                st.success(f"💬 Réponse : {answer}")
