import os
import msvcrt, os, time

def read_txt_config():
    """Read host, user, and password from a TXT file."""
    config = {}
    try:
        with open("config.txt", 'r') as file:
            for line in file:
                key, value = line.strip().split('=')
                config[key] = value

        host = config.get('host')
        user = config.get('user')
        password = config.get('password')
        database = config.get("database")
        
        return host, user, password, database

    except Exception as e:
        print(f"Error reading the config file: {e}")
        return None, None, None


def clear_screen():
    # Clear the terminal screen
    os.system('cls' if os.name == 'nt' else 'clear')

def print_centered(text):
    # Calculate the width of the terminal
    width = os.get_terminal_size().columns
    # Center the text and print it
    print(text.center(width, ' '))

def print_bordered(text):
    # Create a border around the text
    width = os.get_terminal_size().columns
    border_line = '*' * width
    print(border_line)
    print_centered(text)
    print(border_line)

def title_page(role):
    clear_screen()  # Clear the screen
    print_bordered("Welcome to Healthcare Center")  # Print the welcome message
    print("\n")  # Add some spacing
    print_centered(f"{role}")  # Print the doctor's login page heading
    print("\n")  # Add some spacing


def display_menu(options, current_option):
    for idx, option in enumerate(options):
        if idx == current_option:
            print(f"> {option} <")  # Highlight current option
        else:
            print(f"  {option}")


def userchoise(id):
    from pat_login import log_pat
    from doc_login import log_doc
    from doc_registration import doctor_registration
    from pat_registration import patient_registration
    
    os.system("cls")
    
    options = ['Login', 'Register', 'Exit']
    current_option = 0

    while True:
        print_bordered("Welcome to Healthcare Center")
        print("\n\n")

        print("\nSelect an option:")
        display_menu(options, current_option)

        # Wait for a key press
        key = msvcrt.getch()

        if key == b'\xe0':  # Special keys start with escape character
            os.system("cls")
            key = msvcrt.getch()  # Get the actual arrow key press
            if key == b'H':  # Up arrow
                if current_option > 0:
                    current_option -= 1
            elif key == b'P':  # Down arrow
                if current_option < len(options) - 1:
                    current_option += 1
        elif key == b'\r':  # Enter key
            print(f"\nYou selected: {options[current_option]}")
            
            if current_option == 0:
                if id == "p": log_pat()
                else: log_doc()
            
            if current_option == 1:
                if id == "p": patient_registration()
                else: doctor_registration()

            if current_option == 2:  # If Exit is selected
                print("Exiting the program...")
                os.system("cls")
                break


