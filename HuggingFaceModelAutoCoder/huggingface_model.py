from transformers import AutoModelForCausalLM, AutoTokenizer
import re

def initialize_model(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer.pad_token = tokenizer.eos_token
    return tokenizer, model

def generate_code(tokenizer, model, prompt):
    inputs = tokenizer(prompt, return_tensors="pt", padding=True, truncation=True)
    attention_mask = inputs.attention_mask
    input_ids = inputs.input_ids

    outputs = model.generate(input_ids, attention_mask=attention_mask, max_length=100, num_return_sequences=1)
    raw_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    code = re.sub(r'#.*|\n\s*#.*', '', raw_code).strip()
    
    return code if "import" in code or "def" in code else None  # Basic validation
