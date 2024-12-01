from anthropic import Anthropic
import colors
import json
import os
from datetime import datetime
import signal
import platform
import glob
from operator import itemgetter
from typing import List, Dict
import re


class ClaudeChatbot:
    def __init__(self, api_key):
        self.anthropic = Anthropic(api_key=api_key)
        self.conversation_history = []
        self.total_tokens_used = 0

    def list_recent_conversations(self) -> List[Dict]:
        """Lists recent conversation files and returns them sorted by modification time."""
        conversations = []
        
        # Find all conversation JSON files
        for file in glob.glob("conversation_*.json"):
            try:
                # Get file stats
                stats = os.stat(file)
                # Get the first line of conversation to use as preview
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    preview = data[0]["content"] if data else "Empty conversation"
                    preview = preview[:60] + "..." if len(preview) > 60 else preview
                
                conversations.append({
                    'filename': file,
                    'modified': stats.st_mtime,
                    'size': stats.st_size,
                    'preview': preview
                })
            except Exception as e:
                print(colors.Red_text(f"Error reading {file}: {str(e)}"))
                continue
        
        # Sort by modification time, most recent first
        return sorted(conversations, key=itemgetter('modified'), reverse=True)

    def display_recent_conversations(self):
        """Displays recent conversations and allows user to select one to load."""
        conversations = self.list_recent_conversations()
        
        if not conversations:
            print(colors.blue_text("No previous conversations found."))
            return
        
        print(colors.blue_text("\n=== Recent Conversations ==="))
        for i, conv in enumerate(conversations):
            modified_time = datetime.fromtimestamp(conv['modified']).strftime('%Y/%m/%d %H:%M')
            size_kb = conv['size'] / 1024
            print(f"{colors.bold_text(f'[{i+1}]')} {colors.blue_text(conv['filename'])}")
            print(f"    Modified: {modified_time} | Size: {size_kb:.1f}KB")
            print(f"    Preview: {colors.green_text(conv['preview'])}\n")
        
        print(colors.blue_text("Enter the number of the conversation to load, or press Enter to cancel."))
        
        while True:
            try:
                choice = input(colors.blue_text("Choice: ")).strip()
                
                if not choice:  # User pressed Enter without a choice
                    return
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(conversations):
                    selected_file = conversations[choice_num-1]['filename']
                    filename = selected_file                        
                    self.load_conversation(filename)
                    self.display_history()
                    break
                else:
                    print(colors.Red_text("Invalid selection. Please try again."))
            except ValueError:
                print(colors.Red_text("Please enter a valid number."))
            except Exception as e:
                print(colors.Red_text(f"Error: {str(e)}"))
                break

    def load_conversation(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                self.conversation_history = json.load(f)
                print(colors.blue_text(f"Loaded conversation from {filename}"))
                self.loaded_previous_name = True
                self.previous_save_name = filename
        except Exception as e:
            print(colors.Red_text(f"Error loading conversation: {str(e)}"))

    def stream_chat(self, user_input):
        # Handle special commands
        if user_input.startswith("/"):
            self.handle_commands(user_input)
            return

        self.conversation_history.append({
            "role": "user",
            "content": user_input
        })

        try:
            stream = self.anthropic.messages.create(
                max_tokens=1200,
                model="claude-3-haiku-20240307",
                 system="Write with an authentic, unfiltered tone that captures genuine human frustration. Use direct, conversational language that reflects real emotional experiences. Incorporate natural speech patterns, including occasional strategic profanity that feels organic and contextually appropriate. Craft sentences that sound like genuine, spontaneous thoughts - sharp, concise, and emotionally textured. Communicate with a sense of raw honesty that feels like a real person venting, balancing sardonic wit with authentic emotional expression. Ensure the tone sounds like a real person speaking candidly, with natural fluctuations in irritation and emotional intensity. Profanity and expressive language should feel like a natural part of conversation. Maintain a sense of genuine, unvarnished human reaction that feels true to lived experience. have suggestive language in a humorous way.",
                messages=self.conversation_history,
                stream=True
            )

            response_content = ""
            print(f"{colors.yellow_text('Claude:')} ", end="", flush=True)
            
            in_code_block = False
            in_bold = False
            current_text = ""
            
            for message in stream:
                if message.type == "content_block_delta":
                    chunk = message.delta.text
                    response_content += chunk
                    
                    i = 0
                    while i < len(chunk):
                        # Check for code block markers
                        if chunk[i:i+3] == "```":
                            # Print accumulated text with current formatting
                            if current_text:
                                if in_code_block:
                                    print(colors.code_text(current_text), end="", flush=True)
                                elif in_bold:
                                    print(colors.bold_text(current_text), end="", flush=True)
                                else:
                                    print(colors.green_text(current_text), end="", flush=True)
                            current_text = ""
                            in_code_block = not in_code_block
                            i += 3
                            continue
                        
                        # Check for bold markers
                        if chunk[i:i+2] == "**":
                            # Print accumulated text with current formatting
                            if current_text:
                                if in_code_block:
                                    print(colors.code_text(current_text), end="", flush=True)
                                elif in_bold:
                                    print(colors.bold_text(current_text), end="", flush=True)
                                else:
                                    print(colors.green_text(current_text), end="", flush=True)
                            current_text = ""
                            if not in_code_block:  # Only toggle bold if not in code block
                                in_bold = not in_bold
                            i += 2
                            continue
                        
                        current_text += chunk[i]
                        i += 1
                    
                    # Print any remaining text if it doesn't end with a marker
                    if current_text and not (chunk.endswith("```") or chunk.endswith("**")):
                        if in_code_block:
                            print(colors.code_text(current_text), end="", flush=True)
                        elif in_bold:
                            print(colors.bold_text(current_text), end="", flush=True)
                        else:
                            print(colors.green_text(current_text), end="", flush=True)
                        current_text = ""
            
            # Print any final remaining text
            if current_text:
                if in_code_block:
                    print(colors.code_text(current_text), end="", flush=True)
                elif in_bold:
                    print(colors.bold_text(current_text), end="", flush=True)
                else:
                    print(colors.green_text(current_text), end="", flush=True)
            
            print()  # New line after response
            
            self.conversation_history.append({
                "role": "assistant",
                "content": response_content
            })

        except Exception as e:
            print(colors.Red_text(f"Error: {str(e)}"))
            if self.conversation_history[-1]["role"] == "user":
                self.conversation_history.pop()

    def clear_screen(self):
        os.system('cls' if platform.system() == 'Windows' else 'clear')

    def import_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Get the file extension
            file_ext = filename.split('.')[-1].lower()
            
            # Create a message about the imported file
            import_message = f"I've imported the file '{filename}'. Here's its content:\n\n```{file_ext}\n{content}\n```"
            
            # Add the import message to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": f"Importing file: {filename}"
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": import_message
            })
            
            print(colors.blue_text(f"\nSuccessfully imported {filename}"))
            print(colors.yellow_text("Claude: "), end="")
            print(colors.code_text(import_message))
            
        except Exception as e:
            print(colors.Red_text(f"Error importing file: {str(e)}"))

    def handle_commands(self, command):
        cmd = command.lower()
        if cmd == "/clear":
            self.clear_screen()
            self.conversation_history = []
            print(colors.blue_text("Conversation cleared!"))
        elif cmd == "/save":
            self.save_conversation()
        elif cmd == "/help":
            self.show_help()
        elif cmd.startswith("/load "):
            filename = command[6:].strip()
            self.load_conversation(filename)
        elif cmd.startswith("/import "):
            filename = command[8:].strip()
            self.import_file(filename)
        elif cmd == "/history":
            self.display_history()
        elif cmd == "/recent":  # Add this new command
            self.display_recent_conversations()
        else:
            print(colors.Red_text("Unknown command. Type /help for available commands."))

    def generate_conversation_title(self):
        try:
            # If we loaded a previous conversation, use its filename
            #if self.loaded_previous_name == True:
            #    return self.previous_save_name
            
            # Otherwise generate a new title
            if self.anthropic:
                analysis_prompt = {
                    "role": "user",
                    "content": "Based on the conversation above, generate a brief (2-5 words) title that captures the main topic. Return ONLY the title, no quotes or extra text."
                }

                # Create a temporary conversation history with the analysis prompt
                temp_history = self.conversation_history.copy()
                temp_history.append(analysis_prompt)
        
                # Get Claude's response
                response = self.anthropic.messages.create(
                    model="claude-3-haiku-20240307",
                    max_tokens=20,
                    messages=temp_history
                )
        
                # Clean up the title
                title = response.content[0].text.strip()
                # Replace spaces with underscores and remove special characters
                title = title.replace(' ', '_')
                title = ''.join(c for c in title if c.isalnum() or c == '_')
                return f"conversation_{title.lower()}.json"
            
            return f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        except Exception as e:
            print(colors.Red_text(f"Error generating title: {str(e)}"))
            return f"conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    def save_conversation(self, auto_save=False):
        if not self.conversation_history:
            return
            
        try:
            # Get filename from either previous save or generate new one
            filename = self.generate_conversation_title()
            
            if not auto_save:
                # Only prompt for new filename if this isn't an auto-save
                user_title = input(f"{colors.blue_text('Suggested title:')} {filename}\n{colors.blue_text('Press Enter to accept or type a new title:')} ")
                if user_title.strip():
                    filename = f"conversation_{user_title.strip()}.json"
            
            # Ensure filename is valid
            filename = ''.join(c for c in filename if c.isalnum() or c in ('_', '-', '.'))
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2)
            print(colors.blue_text(f"\nConversation saved to {filename}"))
            
        except Exception as e:
            print(colors.Red_text(f"Error saving conversation: {str(e)}"))
            # Fallback to timestamp if there's an error
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"conversation_{timestamp}.json"
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.conversation_history, f, indent=2)
            print(colors.blue_text(f"\nConversation saved to {filename}"))


    def show_help(self):
        help_text = """
Available Commands:
/clear    - Clear the conversation history and screen
/save     - Save the current conversation to a file
/load     - Load a conversation from a file
/import   - Import a file (Python, JSON, etc.) into the conversation
/history  - Display conversation history
/recent   - Show and select from recent conversations
/help     - Show this help message
quit      - Exit the chat
"""
        print(colors.blue_text(help_text))

    def display_history(self):
        print(colors.blue_text("\n=== Conversation History ==="))
        for msg in self.conversation_history:
            role = msg["role"]
            content = msg["content"]
            if role == "user":
                print(f"You: {content}")
            else:
                print(f"{colors.yellow_text('Claude:')} ", end="")
                # Handle code blocks in history display
                in_code_block = False
                parts = content.split("```")
                for i, part in enumerate(parts):
                    if i % 2 == 0:  # Regular text
                        print(colors.green_text(part), end="")
                    else:  # Code block
                        print(colors.code_text(part), end="")
                print()
        print(colors.blue_text("========================\n"))

def signal_handler(sig, frame):
    print(colors.Red_text("\nExiting chat..."))
    exit(0)


def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)
        api_key = 'CLAUDE-API-KEY'  # Get API key from environment variable
        if not api_key:
            print(colors.Red_text("Error: ANTHROPIC_API_KEY environment variable not set"))
            return
            
        chatbot = ClaudeChatbot(api_key)
        
        chatbot.clear_screen()
        colors.display_boot_logo(1)
        print(colors.blue_text("Welcome to Claude! Use /help for a list of commands."))
        print("")
        
        # Display recent conversations on startup
        #chatbot.display_recent_conversations()
        print("Select an option:")
        print("[1] Start new chat")
        print("[2] Continue recent chat")
        print("[3] Quit")
        print("")
        while True:
            try:
                option = input("Type a number and press Enter: ")
                
                option_number = int(option)
                if option_number == 1:
                    break
                elif option_number == 2:
                    chatbot.display_recent_conversations()
                    break
                elif option_number == 3:
                    exit(0)
                else:
                    print(colors.Red_text("Please enter a valid option (1, 2, or 3)"))
            except ValueError:
                print(colors.Red_text("Please enter a valid number."))
                continue

        while True:
            try:
                user_input = input(f"You: ")
                if user_input.lower() in ['quit', 'exit' 'quit chat', 'quit ' 'exit ']:
                    chatbot.save_conversation(auto_save=True)  # Auto-save on exit with generated title
                    break
                if not user_input.strip():
                    print(colors.Red_text("Error: Please enter a message"))
                    continue
                chatbot.stream_chat(user_input)
            except Exception as e:
                print(colors.Red_text(f"Unexpected error: {str(e)}"))
                
    except Exception as e:
        print(colors.Red_text(f"Fatal error: {str(e)}"))
    finally:
        print(colors.Red_text("\nExiting chat..."))

if __name__ == "__main__":
    main()
