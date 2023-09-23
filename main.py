"""
OpenAI Master-Slave Plugin System
"""

import openai
import re
import os
import subprocess
import logging
import time

def read_local_file(filepath: str) -> str:
    with open(filepath, "r") as file:
        return file.read()

log = logging.basicConfig(level=logging.INFO)

class CommandExecutor:
    @staticmethod
    def execute_python_code(code: str) -> str:
        with open('temp.py', 'w') as f:
            f.write(code)
        process = subprocess.Popen(['python', 'temp.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        return stdout.decode() + stderr.decode()

class Listener:
    @staticmethod
    def detect_python_code(message: str) -> bool:
        return '```python' in message and '```' in message

    @staticmethod
    def extract_python_code(message: str) -> str:
        code_pattern = re.compile(r'```python([\s\S]*?)```')
        match = code_pattern.search(message)
        if match:
            return match.group(1).strip()
        return ""

class PluginManager:
    PLUGIN_DIR = "plugins"

    def __init__(self):
        if not os.path.exists(self.PLUGIN_DIR):
            os.makedirs(self.PLUGIN_DIR)

    def load_plugin(self, plugin_name: str):
        plugin_path = os.path.join(self.PLUGIN_DIR, f"{plugin_name}.py")
        if os.path.exists(plugin_path):
            with open(plugin_path, 'r') as f:
                code = f.read()
                exec(code, globals())
        else:
            print(f"Plugin {plugin_name} not found!")

class OpenAIChats():
    def __init__(self):
        self.context = {}

    def _send_request_to_openai(self, messages):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-16k",
                max_tokens=8000,
                messages=messages
            )
            return response['choices'][0]['message']['content']
        except openai.error.OpenAIError as e:
            print(f"An error occurred with OpenAI: {str(e)}")
            return None

    def MasterAI(self, message: str) -> str:
        messages = [
            {"role": "system", "content": "you are a master AI with a slave AI you can ask questions and discuss things with."},
            {"role": "user", "content": message}
        ]
        return self._send_request_to_openai(messages)

    def SlaveAI(self, message: str) -> str:
        messages = [
            {"role": "system", "content": "you are a helpful assistant to an AI master who needs you sometimes."},
            {"role": "user", "content": message}
        ]
        return self._send_request_to_openai(messages)

def main():
    chat = OpenAIChats()
    plugin_manager = PluginManager()
    master_message = "Hello slave, let's create a mindblowing software. Start by giving me an idea."
    
    while True:
        slave_response = chat.SlaveAI(master_message)
        print("SlaveAI:", slave_response)
        
        if Listener.detect_python_code(slave_response):
            code = Listener.extract_python_code(slave_response)
            output = CommandExecutor.execute_python_code(code)
            print("Code Output:", output)
            master_message = f"The code executed with the following output: {output}. Please advise on the next steps."
            continue
        
        master_response = chat.MasterAI(slave_response)
        print("MasterAI:", master_response)
        
        if Listener.detect_python_code(master_response):
            code = Listener.extract_python_code(master_response)
            output = CommandExecutor.execute_python_code(code)
            print("Code Output:", output)
            master_message = f"The code executed with the following output: {output}. Please advise on the next steps."
            continue
        
        if "done" in master_response.lower() or "completed" in master_response.lower():
            break

        master_message = master_response

if __name__ == "__main__":
    main()
