import mysql.connector
from mysql.connector import Error
from commands import title_page, print_bordered, display_menu, read_txt_config
import os, msvcrt, time


def connect_server_connection():

    host, user, password, database = read_txt_config()
    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
        if connection.is_connected():
            print("\nServer Connected\n\n")
            return connection
    except Error as err:
        print(f"Error: {err}")
        return None


def register(query, connection, values):
    status = ""
    try:
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        print("doctor registered successfully!")
        time.sleep(3)
        os.system("cls")

        status = "ok"


    except Error as err:
        print(f"Error: {err}")
        status = "doctor Not Registered"

    finally:
        cursor.close()

    return status


def doctor_registration():    
    connection = connect_server_connection()
    if connection is None:
        print("Failed to connect to the database.")
        return

    title_page("Doctor's Registration")

    options = ["First Name", "Last Name","Contact Number", "Email", "Gender", "Specialization", "Next Availability?(dd-mm-yy)"]
    result = []
    values = ()

    print("\nPlease enter your details\n")

    for i in range(len(options)):
        val = input(f"{options[i]}: ")
        values += (val,)
        result.append(val)

    values += ("None",)

    query = """
    INSERT INTO Doctor_Rec 
    (FirstName, LastName, ContactNumber, Email, Gender, Specialization, Availability, Appointments) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    choices = ['Register', 'Redo', 'Exit']
    current_option = 0

    os.system("cls")
    
    while True:

        print_bordered("Doctor's Registration")

        print("\n\nPlease confirm the details\n")
        for i in range(len(options)):
            print(f"{options[i]}: {result[i]}")

        print("\n\n")

        display_menu(choices, current_option)

        # Wait for a key press
        key = msvcrt.getch()

        if key == b'\xe0':  # Special keys start with escape character
            os.system("cls")
            key = msvcrt.getch()  # Get the actual arrow key press
            if key == b'H':  # Up arrow
                if current_option > 0:
                    current_option -= 1
            elif key == b'P':  # Down arrow
                if current_option < len(choices) - 1:
                    current_option += 1
        elif key == b'\r':  # Enter key
            print(f"\nYou selected: {choices[current_option]}")

            if current_option == 0:  # Register option
                stat = register(query, connection, values)
                if stat == "ok":
                    break
                else:
                    input("")

            if current_option == 1:  # Redo option
                os.system("cls")
                doctor_registration()

            if current_option == 2:  # Exit option
                print("Exiting the program...")
                os.system("cls")
                break

    connection.close()


# doctor_registration()
