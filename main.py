import openai
import re
import os
import logging
import tempfile
import asyncio
import json
from contextlib import contextmanager
import tkinter as tk
from tkinter import scrolledtext, Button, Label, OptionMenu, StringVar
import threading
import chat as AIChat
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

# moved to its own plugin.py


async def main():
    config = load_or_create_config()
    master_chat = AIChat("you are a MasterAI named Fred that specializes in automation with python logic and functions you make with your assistant.", config['openai_api_key'])
    slave_chat = AIChat("you are a helpful python coding expert assistant to an AI master who needs you to analyze and refactor any code to improve it by 2x its current functionalities adding classes and logic to delve deeper into its user case. ask if the masterAI has a vision, if not help provide one for the future of it explaining in detail..", config['openai_api_key'])
    plugin_manager = PluginManager()
    plugin_manager.load_all_plugins()
    master_message = "Hello to you my new collegue, let's create a mindblowing software in python code. Start by giving me an idea alongside a python script, this should be our desired format."
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
