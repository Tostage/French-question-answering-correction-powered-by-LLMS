import streamlit as st
from qa_model import load_french_llm, generate_answer
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="French QA Correction App", layout="wide")

if "pipe" not in st.session_state:
    st.session_state.pipe = load_french_llm()

st.title("🇫🇷 French Question Answering & Correction App")
st.markdown("Evaluate LLM answers, correct them, and export as CSV.")

# Load sample questions
def load_questions():
    if os.path.exists("sample_questions.txt"):
        with open("sample_questions.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    return []

sample_questions = load_questions()

# Session Data
if "output_rows" not in st.session_state:
    st.session_state.output_rows = []

# Sidebar
st.sidebar.header("Options")
selected_question = st.sidebar.selectbox("Choose a sample question", [""] + sample_questions)
custom_question = st.sidebar.text_input("Or enter your own:", "")

# Main interaction
question = custom_question if custom_question.strip() else selected_question

if question:
    st.subheader("📌 Question")
    st.write(question)

    if st.button("Generate Answer"):
        with st.spinner("Generating..."):
            llm_response = generate_answer(st.session_state.pipe, question)
            st.session_state.last_response = llm_response

if "last_response" in st.session_state:
    st.subheader("🤖 LLM Response")
    st.write(st.session_state.last_response)

    st.subheader("🛠 Manual Correction")
    correction = st.text_area("Enter your correction (if any):", "")
    mistake_flag = st.checkbox("Flag as mistake?", value=False)

    if st.button("Save Response"):
        entry = {
            "question": question,
            "llm_response": st.session_state.last_response,
            "correction": correction,
            "mistake_flag": "yes" if mistake_flag else "no",
            "timestamp": datetime.now().isoformat()
        }
        st.session_state.output_rows.append(entry)
        st.success("Saved!")

if st.session_state.output_rows:
    st.subheader("📤 Export Responses")
    df = pd.DataFrame(st.session_state.output_rows)
    st.dataframe(df)

    if st.button("Export to CSV"):
        df.to_csv("outputs.csv", index=False, encoding="utf-8")
        st.success("Exported to outputs.csv ✅")
