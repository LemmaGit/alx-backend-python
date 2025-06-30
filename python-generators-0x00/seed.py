import csv
import uuid
import mysql.connector
from mysql.connector import Error

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password'  # Change to your MySQL password
}

# CSV file path
CSV_FILE = 'user_data.csv'

def connect_db():
    """Connect to the MySQL database server"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        print("Connected to MySQL server successfully")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_database(connection):
    """Create the ALX_prodev database if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created or already exists")
    except Error as e:
        print(f"Error creating database: {e}")

def connect_to_prodev():
    """Connect to the ALX_prodev database"""
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database='ALX_prodev'
        )
        print("Connected to ALX_prodev database successfully")
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def create_table(connection):
    """Create the user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL(3,1) NOT NULL,
                INDEX (user_id)
            )
        """)
        print("Table user_data created or already exists")
    except Error as e:
        print(f"Error creating table: {e}")

def insert_data(connection, data):
    """Insert data into the user_data table if it doesn't exist"""
    try:
        cursor = connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT user_id FROM user_data WHERE user_id = %s", (data['user_id'],))
        if cursor.fetchone():
            print(f"User {data['user_id']} already exists - skipping")
            return
        
        # Insert new data
        cursor.execute("""
            INSERT INTO user_data (user_id, name, email, age)
            VALUES (%s, %s, %s, %s)
        """, (data['user_id'], data['name'], data['email'], data['age']))
        
        connection.commit()
        print(f"Inserted user {data['user_id']}")
    except Error as e:
        print(f"Error inserting data: {e}")

def read_csv_data():
    """Read data from CSV file and yield each row as a dictionary"""
    with open(CSV_FILE, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Convert age to decimal and generate UUID if not provided
            processed_row = {
                'user_id': row.get('user_id', str(uuid.uuid4())),
                'name': row['name'],
                'email': row['email'],
                'age': float(row['age'])
            }
            yield processed_row

def stream_users(connection):
    """Generator that streams rows from the database one by one"""
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")
    
    while True:
        row = cursor.fetchone()
        if row is None:
            break
        yield row
    
    cursor.close()

def main():
    # Setup database and table
    connection = connect_db()
    if connection:
        create_database(connection)
        connection.close()
    
    prodev_connection = connect_to_prodev()
    if prodev_connection:
        create_table(prodev_connection)
        
        # Insert data from CSV
        for user_data in read_csv_data():
            insert_data(prodev_connection, user_data)
        
        # Demonstrate streaming
        print("\nStreaming users from database:")
        user_stream = stream_users(prodev_connection)
        for user in user_stream:
            print(f"Streamed user: {user['name']} (ID: {user['user_id']})")
        
        prodev_connection.close()

if __name__ == "__main__":
    main()