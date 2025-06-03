from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

def load_french_llm():
    model_id = "HuggingFaceH4/zephyr-7b-beta"
    
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=200, do_sample=True)
    return pipe

def generate_answer(pipe, prompt):
    result = pipe(prompt, return_full_text=False)
    return result[0]["generated_text"].strip()
