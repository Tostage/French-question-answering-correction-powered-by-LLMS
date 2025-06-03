from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


def load_french_llm():
    model_id = "HuggingFaceH4/zephyr-7b-beta"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return pipe


def answer_question(pipe, question):
    prompt = f"Corrige la réponse à cette question en français : {question}"
    response = pipe(prompt, max_new_tokens=200, do_sample=True)[0]["generated_text"]
    return response.replace(prompt, "").strip()
