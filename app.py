import os
os.environ["TORCH_ALLOW_TF32_CUDA"] = "0"

import streamlit as st
import pandas as pd
import json
import random
from corrector import correct_french, load_mistakes
from qa_model import load_french_llm, answer_question, load_sample_questions

st.set_page_config(page_title="FrançaisQA", page_icon="🇫🇷")
st.title("🇫🇷 FrançaisQA — Correction + Réponses + Export CSV")

if "pipe" not in st.session_state:
    st.session_state.pipe = load_french_llm()

if "log" not in st.session_state:
    st.session_state.log = []

questions = load_sample_questions()
mistakes = load_mistakes()

tab1, tab2, tab3 = st.tabs(["📝 Correction", "❓ Q&A", "📤 Export"])

# ----- Correction tab -----
with tab1:
    st.subheader("Correction grammaticale")

    if st.button("🔁 Exemple d’erreur"):
        ex = random.choice(mistakes)
        st.session_state.input_text = ex["input"]
        st.session_state.expected = ex["expected"]
        st.experimental_rerun()

    text_input = st.text_area("Texte à corriger :", value=st.session_state.get("input_text", ""))
    
    if st.button("Corriger"):
        corrected, explanations = correct_french(text_input)
        st.success(f"✅ Correction : {corrected}")
        for exp in explanations:
            st.markdown(f"- **Erreur**: `{exp['error']}` → {exp['message']}")
            if exp["suggestions"]:
                st.markdown(f"  - **Suggestions**: {', '.join(exp['suggestions'])}")
        if "expected" in st.session_state:
            st.info(f"🎯 Correction attendue : {st.session_state.expected}")
        st.session_state.log.append({
            "type": "correction",
            "input": text_input,
            "output": corrected
        })

# ----- QA tab -----
with tab2:
    st.subheader("Question en français")

    if st.button("🎲 Question aléatoire"):
        st.session_state.question = random.choice(questions)
        st.experimental_rerun()

    user_q = st.text_input("Posez votre question :", value=st.session_state.get("question", ""))
    
    if st.button("Répondre"):
        with st.spinner("Génération..."):
            answer = answer_question(st.session_state.pipe, user_q)
        st.success(f"💬 Réponse : {answer}")
        st.session_state.log.append({
            "type": "question",
            "input": user_q,
            "output": answer
        })

# ----- Export tab -----
with tab3:
    st.subheader("Exporter les résultats")
    if st.session_state.log:
        df = pd.DataFrame(st.session_state.log)
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger CSV", data=csv, file_name="corrections_log.csv", mime="text/csv")
    else:
        st.info("Aucun résultat à exporter.")
