from gpt4all import GPT4ALL

class Chat:
    def __init__(self, model):
        self.model = model

    def gen(self, prompt):
        response = self.model.generate(prompt, temp=0.3, max_tokens=300)
        if response is not None:
            return response
