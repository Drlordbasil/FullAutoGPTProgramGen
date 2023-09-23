# ContextPlugin.py

from collections import deque

class ContextPlugin:
    def __init__(self, max_length=5):
        self.context_queue = deque(maxlen=max_length)

    def update_context(self, message):
        self.context_queue.append(message)

    def get_context(self):
        return list(self.context_queue)

# Monkey-patch the AIChat class to include context management
original_chat_executor = AIChat.chat

async def new_chat_executor(self, message):
    if not hasattr(self, 'context_plugin'):
        self.context_plugin = ContextPlugin()

    self.context_plugin.update_context(message)
    context_messages = self.context_plugin.get_context()

    system_message = {
        "role": "system",
        "content": f"{self.role_description}. Your task is to engage in a complex dialogue about Python programming, including generating Python code snippets that solve specific problems."
    }

    user_message = {
        "role": "user",
        "content": f"{message}. Please provide a Python code snippet that demonstrates your solution, and explain the logic behind it."
    }

    messages = [system_message] + [{"role": "user", "content": msg} for msg in context_messages]

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

AIChat.chat = new_chat_executor
