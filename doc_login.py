import mysql.connector
from mysql.connector import Error
from commands import title_page, print_bordered, display_menu, read_txt_config
import os, time, msvcrt
from prettytable import PrettyTable

connection = None
cursor = None
check= " "


def connect_server_connection():
    global connection, cursor

    host, user, password, database = read_txt_config()

    try:
        connection = mysql.connector.connect(host=host, user=user, passwd=password, database=database)
        cursor = connection.cursor()
        print("\nServer Connect\n\n")
    except Error as err:
        print(f"Error: ${err}")


def get_Details(qurey, user):
    result = None
    try:
        cursor.execute(qurey,(user,))
        result = cursor.fetchall()

        # Accessing the last element
        pwd_real = result[0][3]
        return result, pwd_real
    
    except Error as err:
        print(f"Error: {err}")

    except IndexError:
        print("Please Check Details")
        time.sleep(3)
        log_doc()


def createTable(headers, rows):
    # Create a table object
    table = PrettyTable()

    # Define column headers
    table.field_names = headers

    for i in range(len(rows)):
        table.add_row(rows[i])

    return table




def login(user, contact, result):
    global connection
    os.system('cls')
    options = ['Check Appointments', 'Edit Details', "Contact Support",'Logout']
    current_option = 0

    name = user + f" {result[0][2]}"
    id, email, gender, specification,  = result[0][0], result[0][4], result[0][5], result[0][6],


    while True:
        print_bordered("Doctor's Details")
        print("\n\n")

        # Print Patient Details
        col1 = ["Name", "Contact", "Gender", "Specification", "Email"]
        col2 = [name, contact, gender, specification, email]

        for i in range(len(col1)):
            print(f"{col1[i]}: {col2[i]}")


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
                check_appointments(id)
                input("\nPress Enter to return to the menu...")
                os.system('cls')
            
            elif current_option == 1:
                print("Edit Details")
                edit_details(id)
                os.system('cls')

            elif current_option == 2:
                print("Contact Support")
                contact_support("doctor", id, user)
                os.system('cls')

            elif current_option == 3:  # If Exit is selected
                print("Exiting the program...")
                os.system("cls")
                connection.close()
                break




# edit details
def edit_details(doctor_id):
    global connection

    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    # Fetch the doctor's current details from the database
    query = "SELECT * FROM Doctor_Rec WHERE DoctorID = %s"
    cursor.execute(query, (doctor_id,))
    doctor_details = cursor.fetchone()

    if doctor_details is None:
        print("Doctor not found.")
        return

    options = ["Contact Number", "Email", "Availability(dd-mm-yy)", "Specialization"]
    fields = ["ContactNumber", "Email", "Availability", "Specialization"]
    
    current_option = 0

    while True:
        os.system("cls")
        print_bordered("Edit Doctor's Details")

        print("\nCurrent Details:")
        print(f"1. Contact Number: {doctor_details[3]}")
        print(f"2. Email: {doctor_details[4]}")
        print(f"3. Availability: {doctor_details[7]}")
        print(f"3. Specialization: {doctor_details[6]}")
        print("\nSelect a detail to edit:")

        display_menu(options, current_option)

        key = msvcrt.getch()
        if key == b'\xe0':  # Special keys like arrow keys
            os.system("cls")
            key = msvcrt.getch()  # Get the actual arrow key press
            if key == b'H':  # Up arrow
                if current_option > 0:
                    current_option -= 1
            elif key == b'P':  # Down arrow
                if current_option < len(options) - 1:
                    current_option += 1
        elif key == b'\r':  # Enter key
            selected_field = fields[current_option]
            new_value = input(f"\nEnter new {options[current_option]}: ")

            update_query = f"UPDATE Doctor_Rec SET {selected_field} = %s WHERE DoctorID = %s"
            try:
                cursor.execute(update_query, (new_value, doctor_id))
                connection.commit()
                print(f"\n{options[current_option]} updated successfully!")
            except Error as err:
                print(f"Error: {err}")

            # Ask if user wants to edit another detail or exit
            if input("Do you want to edit another detail? (y/n): ").lower() != 'y':
                break

    cursor.close()



# contact Support

def contact_support(user_type, user_id, user):
    global connection
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    # Welcome message
    os.system("cls")
    title_page("Contact Support")

    print(f"Hello {user_type.capitalize()} {user.capitalize()}, how can we assist you today?")
    print("\nPlease describe your issue below:")

    # Capture user issue
    issue_description = input("\nIssue description: ")

    # Insert issue into the database
    query = """
    INSERT INTO support_tickets (UserType, UserID, IssueDescription, Status, CreatedAt) 
    VALUES (%s, %s, %s, %s, %s);
    """
    values = (user_type, user_id, issue_description, 'Open', time.strftime('%Y-%m-%d %H:%M:%S'))

    try:
        cursor.execute(query, values)
        connection.commit()
        print("\nThank you for contacting support. Your issue has been submitted.")
        time.sleep(3)

    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()



# Check appointments
def check_appointments(doctor_id):
    global connection
    if connection is None:
        print("Failed to connect to the database.")
        return

    query = """
    SELECT A.AppointmentID, P.FirstName, P.LastName, P.ContactNumber, A.AppointmentDate, A.Status, P.MedicalHistory
    FROM Appointments A
    JOIN patient_rec P ON A.PatientID = P.PatientID
    WHERE A.DoctorID = %s;
    """

    appointment_rows = []
    headers = ["Appointment ID", "Patient", "Contact Number", "Appointment Date", "Status", "Medical History"]

    try:
        cursor = connection.cursor()
        cursor.execute(query, (doctor_id,))
        appointments = cursor.fetchall()

        if appointments:
            print("\nScheduled Appointments:\n")
            for appointment in appointments:
                appointment_rows.append([appointment[0], f"{appointment[1]} {appointment[2]}", appointment[3], appointment[4], appointment[5], appointment[6]])
        else:
            print("No scheduled appointments.")

        if appointment_rows:
            print(createTable(headers, appointment_rows))

    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()





def log_doc():
        global check

        connect_server_connection()
        title_page("Doctor's Login Page")

        print(check+"\n\n")
        print("Please enter your credentials:") 

        user = input("First Name: ")
        pwd = input("Contact: ")

        # user = "jImMy"
        # pwd = "1234567890"

        q1 = f"select * from doctor_rec where FirstName = %s"
        results, pwd_real = get_Details(q1,user)

        if pwd.lower() == pwd_real.lower():
            print("\n\nLogin Successfull")
            time.sleep(1)
            check = ""
            login(user.capitalize(), pwd, results)

        else:
            results=None
            check = "Please Check you Contact info..."
            time.sleep(1)
            log_doc()



# log_doc()