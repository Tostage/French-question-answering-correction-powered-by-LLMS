from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_french_llm():
    model_id = "mistralai/Mistral-7B-Instruct-v0.1"  # Or use Zephyr or Phi
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto")
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return pipe

def answer_question(pipe, question):
    prompt = f"Répondez à la question suivante en français: {question}\nRéponse:"
    result = pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)
    return result[0]['generated_text'].split("Réponse:")[-1].strip()

