import tkinter as tk
from tkinter import scrolledtext
import threading

def show_code_output_popup(output):
    popup = tk.Tk()
    popup.title("Code Output")
    frame = scrolledtext.ScrolledText(popup, wrap=tk.WORD, width=50, height=20)
    frame.pack()
    frame.insert(tk.INSERT, output)
    frame.see(tk.END)
    
    # Auto-close the popup after 5 seconds
    popup.after(5000, popup.destroy)
    
    popup.mainloop()

# Monkey-patch the AIChat class to include code execution and popup
original_chat_executor = AIChat.chat

async def new_chat_executor(self, message):
    response = await original_chat_executor(self, message)
    if '```python' in response and '```' in response:
        code = response.split('```python')[1].split('```')[0].strip()
        output = await execute_python_code(code)
        response += f"\nCode Output:\n{output}"
        
        # Open the popup in a new thread to avoid blocking
        popup_thread = threading.Thread(target=show_code_output_popup, args=(output,))
        popup_thread.start()
        
    return response

AIChat.chat = new_chat_executor
