import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('healthcare.db')
cursor = conn.cursor()

# Create the hospitals table
cursor.execute('''
CREATE TABLE IF NOT EXISTS hospitals (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    beds INTEGER NOT NULL,
    rating REAL NOT NULL
)
''')

# Create the doctors table with a foreign key to hospitals
cursor.execute('''
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL,
    years_experience INTEGER NOT NULL,
    hospital_id INTEGER,
    FOREIGN KEY (hospital_id) REFERENCES hospitals(id)
)
''')

# Create the patients table with a foreign key to doctors
cursor.execute('''
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    age INTEGER NOT NULL,
    ailment TEXT NOT NULL,
    doctor_id INTEGER,
    FOREIGN KEY (doctor_id) REFERENCES doctors(id)
)
''')

# Insert dummy data into the hospitals table
hospitals = [
    ("Penn Medicine", "Philadelphia", 500, 4.5),
    ("UPMC Presbyterian", "Pittsburgh", 600, 4.3),
    ("Jefferson Health", "Philadelphia", 550, 4.4),
    ("Lehigh Valley Hospital", "Allentown", 400, 4.2),
    ("St. Luke's University Hospital", "Bethlehem", 450, 4.3),
    ("Geisinger Medical Center", "Danville", 380, 4.1),
    ("Lancaster General Hospital", "Lancaster", 420, 4.0),
    ("Reading Hospital", "Reading", 410, 4.2),
    ("Hershey Medical Center", "Hershey", 430, 4.4),
    ("Einstein Medical Center", "Philadelphia", 480, 4.1)
]

cursor.executemany('''
INSERT INTO hospitals (name, location, beds, rating)
VALUES (?, ?, ?, ?)
''', hospitals)

# Insert dummy data into the doctors table
doctors = [
    ("Dr. Smith", "Cardiology", 10, 1),
    ("Dr. Johnson", "Neurology", 8, 2),
    ("Dr. Williams", "Orthopedics", 12, 3),
    ("Dr. Brown", "Pediatrics", 5, 4),
    ("Dr. Jones", "Oncology", 15, 5),
    ("Dr. Garcia", "Radiology", 9, 6),
    ("Dr. Martinez", "Nephrology", 7, 7),
    ("Dr. Robinson", "Gastroenterology", 11, 8),
    ("Dr. Clark", "Rheumatology", 6, 9),
    ("Dr. Rodriguez", "Endocrinology", 8, 10)
]

cursor.executemany('''
INSERT INTO doctors (name, specialty, years_experience, hospital_id)
VALUES (?, ?, ?, ?)
''', doctors)

# Insert dummy data into the patients table
patients = [
    ("Alice", 30, "Flu", 1),
    ("Bob", 45, "Back Pain", 2),
    ("Charlie", 28, "Migraine", 3),
    ("David", 50, "High BP", 4),
    ("Eve", 35, "Diabetes", 5),
    ("Frank", 40, "Asthma", 6),
    ("Grace", 32, "Allergies", 7),
    ("Hannah", 60, "Arthritis", 8),
    ("Isaac", 29, "Cold", 9),
    ("Jack", 55, "Heart Problem", 10)
]

cursor.executemany('''
INSERT INTO patients (name, age, ailment, doctor_id)
VALUES (?, ?, ?, ?)
''', patients)

# Commit the changes and close the connection
conn.commit()
conn.close()
