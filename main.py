import msvcrt, os
from commands import print_bordered, display_menu, userchoise

def main():
    options = ['Patient', 'Doctor', 'Exit']
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

            elif key == b'M':  # Condition for create db (Home Key)
                print("Rest")
                if input(": ") == "db":
                    os.system("cls")
                    d = input("Create Database? (y/n): ")
                    if d == "y":
                        from create_databse import main
                        main()
                        print("DB Created")
                        os.system("cls")


        elif key == b'\r':  # Enter key
            print(f"\nYou selected: {options[current_option]}")
            
            if current_option == 0:
                userchoise("p")
            
            if current_option == 1:
                userchoise("d")

            if current_option == 2:  # If Exit is selected
                print("Exiting the program...")
                os.system("cls")
                break


if __name__ == '__main__':
    main()
