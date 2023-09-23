# GPT-3.5 Turbo Master-Slave Conversational Interface with Extensible Plugins

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Components](#components)
8. [Logging and Debugging](#logging-and-debugging)
9. [Use-Cases](#use-cases)
10. [Extending the Project](#extending-the-project)
11. [Contributing](#contributing)
12. [License](#license)

## Introduction

The `GPT-3.5 Turbo Master-Slave Conversational Interface with Extensible Plugins` is a cutting-edge Python application designed to facilitate dynamic conversations between two AI entities: a Master AI and a Slave AI. Utilizing OpenAI's GPT-3.5 Turbo API, the Master AI can initiate dialogues, ask questions, and even execute Python code via the Slave AI. The project is highly modular, featuring a Plugin Manager for seamless integration of additional functionalities and a real-time log viewer for debugging and monitoring.

## Features

- **Master-Slave AI Conversations**: Enables rich dialogues between a Master AI and a Slave AI.
- **Code Execution**: Ability to execute Python code snippets within the conversation.
- **Plugin Manager**: Easily extend the application's capabilities.
- **Real-Time Log Viewer**: Tkinter-based GUI for real-time log monitoring.
  
## Requirements

- **Python 3.7+**: The core language for the project.
- **OpenAI Python package**: For GPT-3.5 Turbo API integration.
- **Tkinter**: For the GUI-based log viewer.
- **asyncio**: For asynchronous programming.
- **re**: For regular expression operations.
- **os**: For operating system dependent functionalities.
- **logging**: For generating log files.
- **tempfile**: For creating temporary files.
- **json**: For handling JSON data.
- **threading**: For multi-threading capabilities.

## Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Drlordbasil/GPTMasterSlaveWithPlugins.git
    ```
2. **Navigate to the Project Directory**:
    ```bash
    cd GPTMasterSlaveWithPlugins
    ```
3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The application uses a `config.json` file to store the OpenAI API key. If the file doesn't exist, it will prompt the user to enter the API key during the first run.

## Usage

Run the `main.py` script to initiate the Master-Slave AI conversation. The log viewer will open in a separate window, displaying real-time logs.

## Components

- **Master AI**: Initiates dialogues, asks questions, and can execute Python code.
- **Slave AI**: Responds to Master AI's queries and executes Python code as instructed.
- **Plugin Manager**: Manages the loading and execution of plugins stored in the `plugins` directory.
- **Log Viewer**: A Tkinter-based GUI for real-time log monitoring.

## Logging and Debugging

The application generates a log file named `ai_chat.log` that stores all the interactions and code execution results. The log viewer provides a real-time view of this log file.

## Use-Cases

- **Automated Software Development**: Master AI can instruct Slave AI to generate code snippets.
- **Data Analysis**: Master AI can ask Slave AI to perform real-time data analysis.
- **Chatbots**: Can be adapted to create more complex chatbot functionalities.
  
## Extending the Project

- **Custom Plugins**: Create custom plugins and place them in the `plugins` directory.
- **Advanced Logging**: Integrate with cloud-based logging solutions.
- **Multi-Agent Systems**: Extend to include more AI agents in the conversation.

## Contributing

Contributions are welcome! Please read the contributing guidelines before making any changes.

## Contact

For any queries or further clarification, feel free to reach out to the project maintainer at [drlordbasil@gmail.com](mailto:drlordbasil@gmail.com).

## Donation

If you find this project useful and would like to support its development, you can make a donation through the following platforms:

- **CashApp**: [$doctorlordbasil](https://cash.app/$doctorlordbasil)
- **PayPal**: [Donate via PayPal](https://paypal.me/chaoticbasil?country.x=US&locale.x=en_US)

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
