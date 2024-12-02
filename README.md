
# Clarde Chatbot

Clarde Chatbot is a powerful command-line interface (CLI) application that allows you to seamlessly interact with the state-of-the-art Anthropic Claude language model. This chatbot offers a wide range of features to enhance your conversational experience, including the ability to save and load conversation history, import external files, and conveniently access your recent discussions.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Starting a New Chat](#starting-a-new-chat)
  - [Continuing a Recent Chat](#continuing-a-recent-chat)
  - [Available Commands](#available-commands)
- [Advanced Features](#advanced-features)
  - [File Imports](#file-imports)
  - [Conversation History Management](#conversation-history-management)
  - [Personalization](#personalization)
- [Configuration](#configuration)
- [Contributing](#contributing)
- [License](#license)

## Installation

1. Make sure you have Python 3.x installed on your system.
2. Install the required dependencies by running the following command in your terminal:
   
   
   pip install colorama anthropic
   
   
3. Obtain an Anthropic API key and set it as an environment variable named `ANTHROPIC_API_KEY`. You can find the link to get your key [here](https://console.anthropic.com/settings/keys).

## Usage

To run Clarde, execute the following command in your terminal:


python clarde.py


If the above command doesn't work, try:


python3 clarde.py


### Starting a New Chat

When you run the script, you'll be prompted to choose an option. Select "1" to start a new chat and begin your conversation with the Anthropic Claude language model.

### Continuing a Recent Chat

If you have saved conversations from previous sessions, you can select "2" to view and load a recent chat, allowing you to pick up where you left off.

### Available Commands

Clarde Chatbot supports a variety of commands to enhance your interaction experience. The following commands are available within the chatbot:

- `/clear`: Clear the conversation history and screen.
- `/save`: Save the current conversation to a file.
- `/load`: Load a conversation from a file.
- `/import`: Import a file (Python, JSON, etc.) into the conversation.
- `/history`: Display the conversation history.
- `/recent`: Show and select from recent conversations.
- `/help`: Display the help message.
- `quit`: Exit the chat.

## Advanced Features

Clarde Chatbot offers several advanced features to streamline your usage and personalize your experience.

### File Imports

The `/import` command allows you to seamlessly incorporate external files, such as code snippets, data sets, or documents, into your conversation. This feature enhances the depth and context of your interactions with the Anthropic Claude language model.

### Conversation History Management

Clarde Chatbot provides robust conversation history management capabilities. You can save your ongoing discussions to files using the `/save` command, and later reload them using the `/load` command. This feature ensures that you can pick up where you left off and maintain the context of your conversations.

### Personalization

Clarde Chatbot can be further customized to suit your preferences. You can modify the application's behavior, appearance, and response styles by adjusting the configuration settings or by contributing to the project's ongoing development.

## Configuration

The script uses the `ANTHROPIC_API_KEY` environment variable to authenticate with the Anthropic API. Make sure to set this variable before running the script.

## Contributing

We welcome contributions from the community to enhance the Clarde Chatbot project. If you have any ideas, bug fixes, or feature enhancements, please feel free to submit a pull request or open an issue on the project's GitHub repository.

## License

This project is licensed under the BSD 3-Clause License.
