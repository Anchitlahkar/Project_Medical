import mysql.connector
from mysql.connector import Error
from commands import read_txt_config

database_name = None

def create_connection():
    """Create a database connection."""

    global database_name
    host, user, password, database = read_txt_config()
    database_name = database

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,  # Update with your database user
            password=password,  # Update with your database password
        )
        if connection.is_connected():
            print("Connected to MySQL server")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection):
    """Create the database if it doesn't exist."""
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created or already exists.")
    except Error as e:
        print(f"Error: {e}")

def create_doctor_table(connection):
    """Create doctor_rec table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS doctor_rec (
        DoctorID INT PRIMARY KEY AUTO_INCREMENT,
        FirstName VARCHAR(100) NOT NULL,
        LastName VARCHAR(100) NOT NULL,
        ContactNumber VARCHAR(15) NOT NULL,
        Email VARCHAR(100) NOT NULL,
        Gender VARCHAR(10) NOT NULL,
        Specialization VARCHAR(100) NOT NULL,
        Availability VARCHAR(255) NOT NULL,
        Appointments TEXT
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'doctor_rec' created.")
    except Error as e:
        print(f"Error: {e}")

def insert_doctors(connection):
    """Insert doctor records into doctor_rec table."""
    insert_doctors_query = """
    INSERT INTO doctor_rec (FirstName, LastName, ContactNumber, Email, Gender, Specialization, Availability, Appointments) 
    VALUES 
    ("Jimmy", "Frank", "1234567890", "jimmy.frank@example.com", "Male", "Cardiology", "10-10-24", NULL),
    ("Marry", "Johnes", "0987654321", "marry.johnes@example.com", "Female", "Cardiology", "08-10-24", NULL),
    ("Shane", "Qert", "1122334455", "shane.qert@example.com", "Male", "Neurology", "08-10-24", NULL),
    ("Quir", "Hyms", "2233445566", "quir.hyms@example.com", "Male", "Neurology", "15-10-24", NULL),
    ("Sara", "Truth", "3344556677", "sara.truth@example.com", "Female", "ENT", "07-10-24", NULL),
    ("James", "Holland", "4455667788", "james.holland@example.com", "Male", "ENT", "12-10-24", NULL);
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_doctors_query)
        connection.commit()
        print("Doctor records inserted into 'doctor_rec'.")
    except Error as e:
        print(f"Error: {e}")

def create_patient_table(connection):
    """Create patient_rec table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS patient_rec(
        PatientID INT PRIMARY KEY AUTO_INCREMENT,
        FirstName VARCHAR(50),
        LastName VARCHAR(50),
        Age INT,
        Gender VARCHAR(10),
        ContactNumber VARCHAR(15),
        Address VARCHAR(255),
        MedicalHistory TEXT,
        Appointment VARCHAR(50)
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'patient_rec' created.")
    except Error as e:
        print(f"Error: {e}")

def insert_patients(connection):
    """Insert patient records into patient_rec table."""
    insert_patients_query = """
    INSERT INTO patient_rec (FirstName, LastName, Age, Gender, ContactNumber, Address, MedicalHistory, Appointment) 
    VALUES 
    ('Emily', 'Johnson', 28, 'Female', '1234567890', '123 Maple Street', 'Asthma', '2024-10-05 10:00'),
    ('Michael', 'Smith', 35, 'Male', '9876543210', '456 Oak Avenue', 'Hypertension', '2024-10-06 11:30'),
    ('Sophia', 'Williams', 24, 'Female', '5556667777', '789 Pine Lane', 'No known medical history', '2024-10-07 09:00'),
    ('James', 'Brown', 42, 'Male', '3334445555', '321 Birch Blvd', 'Diabetes Type 2', '2024-10-08 14:00'),
    ('Olivia', 'Davis', 30, 'Female', '7778889999', '654 Elm Drive', 'Seasonal allergies', '2024-10-09 15:30');
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_patients_query)
        connection.commit()
        print("Patient records inserted into 'patient_rec'.")
    except Error as e:
        print(f"Error: {e}")

def create_appointments_table(connection):
    """Create Appointments table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS Appointments (
        AppointmentID INT PRIMARY KEY AUTO_INCREMENT,
        PatientID INT NOT NULL,
        DoctorID INT NOT NULL,
        AppointmentDate DATETIME NOT NULL,
        Status VARCHAR(20) DEFAULT 'Scheduled',
        CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (PatientID) REFERENCES patient_rec(PatientID),
        FOREIGN KEY (DoctorID) REFERENCES doctor_rec(DoctorID)
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'Appointments' created.")
    except Error as e:
        print(f"Error: {e}")

def insert_appointments(connection):
    """Insert appointment records into Appointments table."""
    insert_appointments_query = """
    INSERT INTO Appointments (PatientID, DoctorID, AppointmentDate) 
    VALUES 
    (1, 1, '2024-10-05 10:00:00'),
    (2, 2, '2024-10-06 11:30:00'),
    (3, 3, '2024-10-07 09:00:00'),
    (4, 4, '2024-10-08 14:00:00'),
    (5, 5, '2024-10-09 15:30:00'),
    (1, 2, '2024-10-07 09:00:00'),
    (2, 1, '2024-10-08 14:00:00'),
    (1, 3, '2024-10-09 15:30:00');
    """
    try:
        cursor = connection.cursor()
        cursor.execute(insert_appointments_query)
        connection.commit()
        print("Appointment records inserted into 'Appointments'.")
    except Error as e:
        print(f"Error: {e}")

def create_support_tickets_table(connection):
    """Create support_tickets table."""
    create_table_query = """
    CREATE TABLE IF NOT EXISTS support_tickets (
        TicketID INT PRIMARY KEY AUTO_INCREMENT,
        UserType VARCHAR(50) NOT NULL,          
        UserID INT NOT NULL,                     
        IssueDescription TEXT NOT NULL,  
        Status VARCHAR(20) DEFAULT 'Open',
        CreatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
        UpdatedAt DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """
    try:
        cursor = connection.cursor()
        cursor.execute(create_table_query)
        print("Table 'support_tickets' created.")
    except Error as e:
        print(f"Error: {e}")

def main():
    global database_name

    connection = create_connection()
    if connection is not None:
        create_database(connection)
        connection.database = database_name  # Switch to the created database
        create_doctor_table(connection)
        insert_doctors(connection)
        create_patient_table(connection)
        insert_patients(connection)
        create_appointments_table(connection)
        insert_appointments(connection)
        create_support_tickets_table(connection)
        connection.close()

if __name__ == "__main__":
    main()