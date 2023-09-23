import openai
import re
import os
import logging
import tempfile
import asyncio
import json
from contextlib import contextmanager
from tkinter import scrolledtext, Button, Label, Tk
from concurrent.futures import ThreadPoolExecutor

logging.basicConfig(level=logging.INFO, filename='ai_chat.log')

@contextmanager
def temp_file(content):
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
        f.write(content)
        temp_name = f.name
    yield temp_name
    os.unlink(temp_name)

async def execute_python_code(code):
    with temp_file(code) as temp_name:
        process = await asyncio.create_subprocess_exec('python', temp_name, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        stdout, stderr = await process.communicate()
    return stdout.decode() + stderr.decode()

def load_or_create_config(file_path='config.json'):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        openai_api_key = input("Enter your OpenAI API key: ")
        config = {"openai_api_key": openai_api_key}
        with open(file_path, 'w') as f:
            json.dump(config, f)
        return config

def detect_python_code(message):
    return '```python' in message and '```' in message

def extract_python_code(message):
    code_pattern = re.compile(r'```python([\s\S]*?)```')
    match = code_pattern.search(message)
    return match.group(1).strip() if match else ""

def auto_refresh_log(frame):
    with open('ai_chat.log', 'r') as f:
        current_log = f.read()
        frame.delete(1.0, Tk.END)
        frame.insert(Tk.INSERT, current_log)
        frame.see(Tk.END)
    frame.after(10000, lambda: auto_refresh_log(frame))

def log_viewer():
    root = Tk()
    root.title("Debugging Log Viewer")
    Label(root, text="Debugging Log").pack()
    frame = scrolledtext.ScrolledText(root, wrap=Tk.WORD, width=100, height=30)
    frame.pack()
    Button(root, text="Manual Refresh", command=lambda: auto_refresh_log(frame)).pack()
    auto_refresh_log(frame)
    root.mainloop()

async def main():
    config = load_or_create_config()
    master_chat = AIChat("you are a master AI with a slave AI you can ask questions and discuss things with.", config['openai_api_key'])
    slave_chat = AIChat("you are a helpful assistant to an AI master who needs you sometimes.", config['openai_api_key'])
    master_message = "Hello to you my new colleague, let's create mind-blowing software in Python code. Start by giving me an idea alongside a Python script, this should be our desired format."
    while True:
        slave_response = await slave_chat.chat(master_message)
        logging.info(f"SlaveAI: {slave_response}")
        if detect_python_code(slave_response):
            code = extract_python_code(slave_response)
            output = await execute_python_code(code)
            logging.info(f"Code Output: {output}")
            master_message = f"The code executed with the following output: {output}. What's next?"
            continue
        master_response = await master_chat.chat(slave_response)
        logging.info(f"MasterAI: {master_response}")
        if detect_python_code(master_response):
            code = extract_python_code(master_response)
            output = await execute_python_code(code)
            logging.info(f"Code Output: {output}")
            master_message = f"The code executed with the following output: {output}. What's next?"
            continue
        if "done" in master_response.lower() or "completed" in master_response.lower():
            break
        master_message = master_response

class AIChat:
    def __init__(self, role_description, api_key):
        self.role_description = role_description
        self.api_key = api_key

    async def chat(self, message):
        messages = [
            {"role": "system", "content": self.role_description},
            {"role": "user", "content": message}
        ]
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
            return None

if __name__ == "__main__":
    with ThreadPoolExecutor() as executor:
        executor.submit(log_viewer)
    asyncio.run(main())
