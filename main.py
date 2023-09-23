import openai
import re
import os
import logging
import tempfile
import asyncio
import json
from contextlib import contextmanager
from github import Github, GithubException
import tkinter as tk
from tkinter import scrolledtext, Button, Label, OptionMenu, StringVar
import threading

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
        frame.delete(1.0, tk.END)
        frame.insert(tk.INSERT, current_log)
        frame.see(tk.END)
    frame.after(10000, lambda: auto_refresh_log(frame))

def manual_refresh(frame):
    with open('ai_chat.log', 'r') as f:
        current_log = f.read()
        frame.delete(1.0, tk.END)
        frame.insert(tk.INSERT, current_log)
        frame.see(tk.END)

def log_viewer():
    root = tk.Tk()
    root.title("Debugging Log Viewer")
    tk.Label(root, text="Debugging Log").pack()
    frame = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=30)
    frame.pack()
    tk.Button(root, text="Manual Refresh", command=lambda: manual_refresh(frame)).pack()
    auto_refresh_log(frame)
    root.mainloop()

class GitHubManager:
    def __init__(self, token):
        self.github = Github(token)
        self.user = self.github.get_user()
    
    def get_or_create_repo(self, repo_name, description=""):
        try:
            repo = self.user.get_repo(repo_name)
        except GithubException:
            repo = self.user.create_repo(repo_name, description=description)
        return repo
    
    def update_file(self, repo, file_path, commit_message, content):
        try:
            file = repo.get_contents(file_path)
            repo.update_file(file.path, commit_message, content, file.sha)
        except GithubException:
            repo.create_file(file_path, commit_message, content)

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

async def main():
    config = load_or_create_config()
    github_manager = GitHubManager("YOUR_GITHUB_TOKEN")
    master_chat = AIChat("You are a master AI with a slave AI you can ask questions and discuss things with.", config['openai_api_key'])
    slave_chat = AIChat("You are a helpful assistant to an AI master who needs you sometimes.", config['openai_api_key'])
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

if __name__ == "__main__":
    log_thread = threading.Thread(target=log_viewer)
    log_thread.start()
    asyncio.run(main())
