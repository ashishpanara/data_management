# Import libraries
import sqlite3

def initialize_db(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    # Get the names of all tables in the database
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    # Drop all tables
    for table_name in tables:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name[0]}")

    # Drop source_students table if it exists
    cursor.execute('''
    DROP TABLE IF EXISTS source_students
    ''')

    # Drop target_students table if it exists
    cursor.execute('''
    DROP TABLE IF EXISTS target_students
    ''')

    # Create source_students table
    cursor.execute('''
    CREATE TABLE source_students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade REAL NOT NULL
    )
    ''')

    # Create target_students table
    cursor.execute('''
    CREATE TABLE target_students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        grade TEXT NOT NULL
    )
    ''')

    # Delete existing records from source_students table
    cursor.execute('''
    DELETE FROM source_students
    ''')

    # Delete existing records from target_students table
    cursor.execute('''
    DELETE FROM target_students
    ''')

    # Insert data into source_students table
    cursor.executemany('''
    INSERT INTO source_students (id, name, age, grade) VALUES (?, ?, ?, ?)
    ''', [
        (1, 'John Doe', 20, 'A'),
        (2, 'Jane Smith', 22, 'B'),
        (3, 'Emily Johnson', 21, 'A'),
        (4, 'Michael Brown', 25, 'C')
    ])

    # Insert the same data into target_students table
    cursor.executemany('''
    INSERT INTO target_students (id, name, age, grade) VALUES (?, ?, ?, ?)
    ''', [
        (1, 'John Doe', 20, 'A'),
        (2, 'Jane Smith', 22, 'B'),
        (3, 'Emily Johnson', 21, 'A'),
        (4, 'Michael Brown', 23, 'C')
    ])

    # Drop source_departments table if it exists
    cursor.execute('''
    DROP TABLE IF EXISTS source_departments
    ''')

    # Create departments table
    cursor.execute('''
    CREATE TABLE source_departments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        head TEXT NOT NULL
    )
    ''')

    # Delete existing records from departments table (truncate)
    cursor.execute('''
    DELETE FROM source_departments
    ''')

    # Insert data into departments table
    cursor.executemany('''
    INSERT INTO source_departments (id, name, head) VALUES (?, ?, ?)
    ''', [
        (1, 'Computer Science', 'Dr. Alan Turing'),
        (2, 'Mathematics', 'Dr. Isaac Newton'),
        (3, 'Physics', 'Dr. Albert Einstein'),
        (4, 'Chemistry', 'Dr. Marie Curie')
    ])

    # Drop source_departments table if it exists
    cursor.execute('''
    DROP TABLE IF EXISTS target_departments
    ''')

    # Create departments table
    cursor.execute('''
    CREATE TABLE target_departments (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        head TEXT NOT NULL
    )
    ''')

    # Delete existing records from departments table (truncate)
    cursor.execute('''
    DELETE FROM target_departments
    ''')

    # Insert data into departments table
    cursor.executemany('''
    INSERT INTO target_departments (id, name, head) VALUES (?, ?, ?)
    ''', [
        (1, 'Computer Science', 'Dr. Alan Turing'),
        (2, 'Mathematics', 'Dr. Isaac Newton'),
        (3, 'Physics', 'Dr. Albert Einstein'),
        (4, 'Chemistry', 'Dr. Marie Curie')
    ])

    conn.commit()
    conn.close()

# Initialize the database with the required tables and data
initialize_db("college.db")