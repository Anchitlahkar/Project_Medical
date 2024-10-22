import mysql.connector
from mysql.connector import Error
from commands import title_page, print_bordered, display_menu,read_txt_config
import msvcrt, os, time
from prettytable import PrettyTable


connection = None
cursor = None
check = ""

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
        pwd_real = result[0][5]
        return result, pwd_real
    
    except Error as err:
        print(f"Error: {err}")

    except IndexError:
        print("Please Check Details")
        time.sleep(3)
        log_pat()


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
    options = ['Book Appointment', 'Check Medical History', 'Edit Details', "Contact Support",'Logout']
    current_option = 0

    appointment_rows = []

    name = user + f" {result[0][2]}"
    id, age, gender, address,  = result[0][0], result[0][3], result[0][4], result[0][6],
    
    q1 = f"select * from appointments where PatientID = %s"
    q2 = f"select * from doctor_rec where DoctorID = %s;"

    try:
        cursor.execute(q1,(id,))
        appointment_details = cursor.fetchall()

        for data in appointment_details:
            cursor.execute(q2,(data[2],))
            doctor_data = cursor.fetchall()

            # print(f"{doctor_data[0][1]} {doctor_data[0][2]}: {doctor_data[0][6]} : {data[3]}")

            # name, specification, appointment date
            appointment_rows.append([f"{doctor_data[0][1]} {doctor_data[0][2]}", doctor_data[0][6], data[3]])


    except Error as err:
        print(f"Error: {err}")


    while True:
        print_bordered("Patient Details")
        print("\n\n")

        # Print Patient Details
        col1 = ["Name", "Contact", "Age", "Gender", "Address"]
        col2 = [name, contact, age, gender, address]

        for i in range(len(col1)):
            print(f"{col1[i]}: {col2[i]}")

        print("\nAppointments:")
        print(createTable(["Appointed Doctor", "Doctors specification" ,"Appointment Dates",],appointment_rows))

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
                print("Book Appointment")
                book_appointment(id)
                input("\n\nReturn...")
                os.system('cls')
            
            elif current_option == 1:
                print("Check Medical History")
                check_medical_history(id)
                input("\n\nReturn...")
                os.system('cls')
            
            elif current_option == 2:
                print("Edit Details")
                edit_patient_details(id)
                os.system('cls')


            elif current_option == 3:
                print("Contact Support")
                contact_support("patient", id, user)
                os.system('cls')

            elif current_option == 4:  # If Exit is selected
                print("Exiting the program...")
                os.system("cls")
                connection.close()
                break
            



# edit details
def edit_patient_details(patient_id):
    global connection

    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    # Fetch the patient's current details from the database
    query = "SELECT * FROM patient_rec WHERE PatientID = %s"
    cursor.execute(query, (patient_id,))
    patient_details = cursor.fetchone()

    if patient_details is None:
        print("Patient not found.")
        return

    options = ["Contact Number", "Address", "Medical History"]
    fields = ["ContactNumber", "Address", "MedicalHistory"]

    current_option = 0

    while True:
        os.system("cls")
        print_bordered("Edit Patient's Details")

        print("\nCurrent Details:")
        print(f"1. Contact Number: {patient_details[5]}")
        print(f"2. Address: {patient_details[6]}")
        print(f"3. Medical History: {patient_details[7]}")
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

            update_query = f"UPDATE patient_rec SET {selected_field} = %s WHERE PatientID = %s"
            try:
                cursor.execute(update_query, (new_value, patient_id))
                connection.commit()
                print(f"\n{options[current_option]} updated successfully!")
            except Error as err:
                print(f"Error: {err}")

            # Ask if the user wants to edit another detail or exit
            if input("Do you want to edit another detail? (y/n): ").lower() != 'y':
                break

    cursor.close()



# Contact Support
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



# book appointment
def book_appointment(patient_id):
    global connection
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    try:
        # Fetching available doctors
        query = "SELECT DoctorID, FirstName, LastName, Specialization FROM doctor_rec"
        cursor.execute(query)
        doctors = cursor.fetchall()

        if doctors:
            print("Available Doctors:\n")
            for idx, doc in enumerate(doctors, start=1):
                print(f"{idx}. Dr. {doc[1]} {doc[2]} - {doc[3]}")
        else:
            print("No doctors available.")
            return

        try:
            # Selecting a doctor
            doctor_choice = int(input("Select a doctor (number): ")) - 1
            selected_doctor = doctors[doctor_choice][0]

            # Getting appointment date and time
            appointment_date = input("Enter appointment date (YYYY-MM-DD): ")
            appointment_time = input("Enter appointment time (HH:MM): ")

            # Constructing the full appointment datetime
            appointment_datetime = f"{appointment_date} {appointment_time}"

            # Inserting into the appointments table
            query = """
            INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate, Status)
            VALUES (%s, %s, %s, 'Scheduled')
            """
            cursor.execute(query, (patient_id, selected_doctor, appointment_datetime))
            connection.commit()
            print("Appointment booked successfully!")

        except IndexError:
            print("Invalid doctor selection. Please try again.")
        
        except Error as err:
            print(f"\n\n Error: {err}")
            print("Try Again!!!")
            time.sleep(3)

    finally:
        cursor.close()


        



# check medical history
def check_medical_history(patient_id):
    global connection
    if connection is None:
        print("Failed to connect to the database.")
        return

    cursor = connection.cursor()

    try:
        query = "SELECT MedicalHistory FROM patient_rec WHERE PatientID = %s"
        cursor.execute(query, (patient_id,))
        medical_history = cursor.fetchone()

        if medical_history:
            print("\nMedical History:")
            print(medical_history[0])  # Assuming medical history is stored as a text field
        else:
            print("No medical history found.")

    except Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()



def log_pat():
    global check


    connect_server_connection()
    title_page("Patient's Login Page")
    
    print(check+"\n")
    print("Please enter your credentials:\n") 
    
    user = input("First Name: ")
    pwd = input("Contact: ")
    
    # user = "eMilY"
    # pwd = "1234567890"

    q1 = f"select * from patient_rec where FirstName = %s"

    try:
        results, pwd_real = get_Details(q1,user)
    except TypeError:
        print("Type error")


    if pwd.lower() == pwd_real.lower():
        print("\n\nLogin Successfull")
        time.sleep(1)
        check = ""
        login(user.capitalize(), pwd, results)

    else:
        results=None
        check = "Please Check you Contact info..."
        time.sleep(1)
        log_pat()



# log_pat()