from huggingface_model import initialize_model, generate_code
from exe_generator import generate_exe

def main():
    model_name = "EleutherAI/gpt-neo-1.3B"  # Corrected model identifier
    use_auth_token = True  # Set to True if you are authenticated
    tokenizer, model = initialize_model(model_name, use_auth_token)
    
    prompt = "Create a Python script for a simple calculator."
    generated_code = generate_code(tokenizer, model, prompt)
    
    with open("generated_code.py", "w") as f:
        f.write(generated_code)
    
    generate_exe("generated_code.py")

if __name__ == "__main__":
    main()
