# Clarde Chatbot

Claude Chatbot is a command-line interface (CLI) application that allows you to interact with the Anthropic Claude language model. This chatbot supports various features, including saving and loading conversation history, importing files, and displaying recent conversations.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Starting a New Chat](#starting-a-new-chat)
  - [Continuing a Recent Chat](#continuing-a-recent-chat)
  - [Available Commands](#available-commands)
- [Configuration](#configuration)
- [License](#license)

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install the required dependencies by running the following command in your terminal:
   
   pip install -r requirements.txt
   
3. Obtain an Anthropic API key and set it as an environment variable named `ANTHROPIC_API_KEY`.

## Usage

To run the Claude Chatbot, execute the following command in your terminal:


python claude-api.py


### Starting a New Chat

When you run the script, you'll be prompted to choose an option. Select "1" to start a new chat.

### Continuing a Recent Chat

If you have saved conversations, you can select "2" to view and load a recent chat.

### Available Commands

The following commands are available within the chatbot:

- `/clear`: Clear the conversation history and screen.
- `/save`: Save the current conversation to a file.
- `/load`: Load a conversation from a file.
- `/import`: Import a file (Python, JSON, etc.) into the conversation.
- `/history`: Display the conversation history.
- `/recent`: Show and select from recent conversations.
- `/help`: Display the help message.
- `quit`: Exit the chat.

## Configuration

The script uses the `ANTHROPIC_API_KEY` environment variable to authenticate with the Anthropic API. Make sure to set this variable before running the script.

## License

This project is licensed under the BSD 3-Clause License.
