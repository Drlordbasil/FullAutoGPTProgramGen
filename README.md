# GPT-3.5-Auto-Conversational-Interface: Master-Slave AI Conversations with Extensible Plugins

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [System Architecture](#system-architecture)
4. [Requirements](#requirements)
5. [Installation](#installation)
6. [Configuration](#configuration)
7. [Usage](#usage)
8. [Components](#components)
9. [Logging and Debugging](#logging-and-debugging)
10. [Advanced Use-Cases](#advanced-use-cases)
11. [Extending the Project](#extending-the-project)
12. [Contributing](#contributing)
13. [Contact](#contact)
14. [Donation](#donation)
15. [License](#license)

## Introduction
GPT-3.5-Auto-Conversational-Interface is a Python application designed to facilitate dynamic, autonomous conversations between two AI entities: a Master AI and a Slave AI. Utilizing OpenAI's GPT-3.5 Turbo API, the Master AI can initiate dialogues, ask questions, and execute Python code via the Slave AI. The project is highly modular, featuring a Plugin Manager for seamless integration of additional functionalities and a real-time log viewer for debugging and monitoring.

## Features

- Master-Slave AI Conversations: Enables rich dialogues between a Master AI and a Slave AI.
- Code Execution: Execute Python code snippets within the conversation.
- Plugin Manager: Extend the application's capabilities with custom plugins.
- Real-Time Log Viewer: Tkinter-based GUI for real-time log monitoring.
- Asynchronous Operations: Utilizes asyncio for efficient task management.
- Regular Expression Support: Utilizes re for advanced text parsing and manipulation.
- Multi-Threading: Uses threading for concurrent operations.

## System Architecture

The project is divided into several Python scripts and modules:

- main.py: The entry point of the application.
- HuggingFaceModelAutoCoder: Directory containing scripts for Hugging Face model operations.
- plugins: Directory for custom plugins.
- requirements.txt: Lists the required Python packages.

## Requirements

- Python 3.7+
- OpenAI Python package
- Tkinter
- asyncio
- re
- os
- logging
- tempfile
- json
- threading

## Installation

\`\`\`bash
git clone https://github.com/Drlordbasil/FullAutoGPTProgramGen.git
cd FullAutoGPTProgramGen
pip install -r requirements.txt
\`\`\`

## Configuration

The application uses a config.json file to store the OpenAI API key. If the file doesn't exist, it will prompt the user to enter the API key during the first run.

## Usage

Run the main.py script to initiate the Master-Slave AI conversation. The log viewer will open in a separate window, displaying real-time logs.

\`\`\`bash
python main.py
\`\`\`

## Components

- Master AI: Initiates dialogues, asks questions, and executes Python code.
- Slave AI: Responds to Master AI's queries and executes Python code as instructed.
- Plugin Manager: Manages the loading and execution of plugins stored in the plugins directory.
- Log Viewer: A Tkinter-based GUI for real-time log monitoring.

## Logging and Debugging

The application generates a log file named ai_chat.log that stores all interactions and code execution results. The log viewer provides a real-time view of this log file.

## Advanced Use-Cases

- Intelligent Code Generation: Master AI can delegate coding tasks to Slave AI.
- Real-Time Data Analytics: Perform real-time data analysis and predictive analytics.
- Advanced Conversational Agents: Create hyper-intelligent conversational agents for various domains.

## Extending the Project

- Custom Plugins: Create custom plugins and place them in the plugins directory.
- Advanced Logging: Integrate with cloud-based logging solutions.
- Multi-Agent Systems: Extend to include more AI agents in the conversation.

## Contributing

Contributions are welcome! Please read the contributing guidelines before making any changes.

## Contact

For any queries or further clarification, feel free to reach out to the project maintainer at drlordbasil@gmail.com.

## Donation

- CashApp: $doctorlordbasil
- PayPal: Donate via PayPal

## License

This project is licensed under the MIT License. See the LICENSE file for details.
