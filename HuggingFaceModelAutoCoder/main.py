from huggingface_model import initialize_model, generate_code
from exe_generator import generate_exe

def main():
    model_name = "eleutherai/gpt-neo-2.7B-code"  # Updated model
    tokenizer, model = initialize_model(model_name)
    
    prompt = "Create a Python script for a simple calculator."
    generated_code = generate_code(tokenizer, model, prompt)
    
    if generated_code:
        with open("generated_code.py", "w") as f:
            f.write(generated_code)
        
        generate_exe("generated_code.py")
    else:
        print("Code generation failed.")

if __name__ == "__main__":
    main()
