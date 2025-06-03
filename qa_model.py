from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_french_llm():
    model_id = "HuggingFaceH4/zephyr-7b-beta"  # Open-access French-compatible
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return pipe

def answer_question(pipe, question):
    prompt = f"Répondez à la question suivante en français : {question}\nRéponse:"
    result = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)
    return result[0]['generated_text'].split("Réponse:")[-1].strip()

def load_sample_questions(path="sample_questions.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
