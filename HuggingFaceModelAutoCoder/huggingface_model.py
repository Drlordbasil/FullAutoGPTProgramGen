from transformers import AutoModelForCausalLM, AutoTokenizer

def initialize_model(model_name, use_auth_token):
    tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=use_auth_token)
    model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=use_auth_token)
    return tokenizer, model

def generate_code(tokenizer, model, prompt):
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(inputs.input_ids, max_length=100)
    generated_code = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return generated_code
