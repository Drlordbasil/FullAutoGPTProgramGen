class AIChat:
    def __init__(self, role_description, api_key):
        self.role_description = role_description
        self.api_key = api_key

    async def chat(self, message):
        system_message = {
            "role": "system",
            "content": f"{self.role_description}. Your task is to engage in a complex dialogue about Python programming, including generating Python code snippets that solve specific problems."
        }
        user_message = {
            "role": "user",
            "content": f"{message}. Please provide a Python code snippet that demonstrates your solution, and explain the logic behind it."
        }

        messages = [system_message, user_message]

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                max_tokens=8000,
                messages=messages,
                api_key=self.api_key
            )
            return response['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"OpenAI Error: {e}")
            return "An error occurred."
