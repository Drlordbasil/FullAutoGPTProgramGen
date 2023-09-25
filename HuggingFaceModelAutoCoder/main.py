from huggingface_model import initialize_model, generate_code
from exe_generator import generate_exe

def main():
    model_name = "gpt-neo-1.3B"  # Change to a suitable model
    tokenizer, model = initialize_model(model_name)
    
    prompt = "Create a Python script for a simple calculator."
    generated_code = generate_code(tokenizer, model, prompt)
    
    with open("generated_code.py", "w") as f:
        f.write(generated_code)
    
    generate_exe("generated_code.py")

if __name__ == "__main__":
    main()
