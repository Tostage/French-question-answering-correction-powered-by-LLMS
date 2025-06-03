from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

def load_french_llm():
    model_id = "HuggingFaceH4/zephyr-7b-beta"  # Change if needed to smaller model like 'google/flan-t5-base'
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_new_tokens=128)
    return pipe

def generate_answer(pipe, question):
    result = pipe(question)
    return result[0]['generated_text'].split("\n")[0]
