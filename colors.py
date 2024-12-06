from colorama import init, Fore, Style

init()

def green_text(text):
    return f"{Fore.GREEN}{text}{Style.RESET_ALL}"

def Red_text(text):
    return f"{Fore.RED}{text}{Style.RESET_ALL}"

def blue_text(text):
    return f"{Fore.BLUE}{text}{Style.RESET_ALL}"

def yellow_text(text):
    return f"{Fore.YELLOW}{text}{Style.RESET_ALL}"

def code_text(text):
    return f"{Style.DIM}{Fore.CYAN}{text}{Style.RESET_ALL}"

def bold_text(text):
    return f"{Style.BRIGHT}{text}{Style.RESET_ALL}"

def display_boot_logo(self):
        logo = f"""{Fore.CYAN}
  
     ░▒▓██████▓▒░░▒▓█▓▒░       ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░ 
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓████████▓▒░▒▓███████▓▒░░▒▓█▓▒░░▒▓█▓▒░▒▓██████▓▒░   
    ░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
    ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░        
     ░▒▓██████▓▒░░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓████████▓▒░ 
                                                                                                                                                            
{Style.RESET_ALL}"""
        print(logo)

if __name__ == "__main__":
    display_boot_logo(1)
    bold_text()
    Red_text()
    green_text()
    blue_text()
    yellow_text()
    code_text()
