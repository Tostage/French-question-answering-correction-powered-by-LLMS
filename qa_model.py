from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

def load_french_llm():
    model_id = "HuggingFaceH4/zephyr-7b-beta"

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    try:
        # Try using accelerate if available
        model = AutoModelForCausalLM.from_pretrained(
            model_id, device_map="auto", torch_dtype="auto"
        )
    except ValueError:
        # Fallback for no accelerate
        model = AutoModelForCausalLM.from_pretrained(model_id)

    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)
    return pipe
