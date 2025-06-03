# FrançaisQA — French Grammar + Question Answering System

This project is a dual-purpose LLM app that:
- ✅ Corrects **French grammar** with detailed suggestions
- ✅ Answers **French-language questions** using an open-source language model
- ✅ Exports results (input + output) to a CSV file for annotation or audit

Built with **Streamlit**, **language-tool-python**, and **Hugging Face Transformers**.


## Features

| Feature                  | Description                                             |
|--------------------------|---------------------------------------------------------|
|  Grammar Correction     | Detects and corrects grammatical/spelling errors        |
|  Question Answering     | LLM answers user-submitted French questions             |
|  Example Generators     | Rotating test inputs from JSON and TXT files            |
|  CSV Export             | Download all session outputs in one click               |

---

## File Structure

French-question-answering-correction-powered-by-LLMS/
├── app.py # Main Streamlit app
├── corrector.py # Grammar correction logic
├── qa_model.py # LLM question answering
├── sample_questions.txt # 10 clean French questions (for QA testing)
├── mistakes.json # 5 broken grammar inputs with expected corrections
└── requirements.txt # All dependencies

## 🛠️ Setup Instructions

### 1. Install Python 3.11 (required)
Do **not use Python 3.13** — it breaks key libraries.

### 2. Install packages
pip install -r requirements.txt

**3. Launch app**
streamlit run app.py
