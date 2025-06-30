import mysql.connector
from mysql.connector import Error

def stream_users():
    """Generator function that streams rows from user_data table one by one"""
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',  # Change to your MySQL password
            database='ALX_prodev'
        )
        
        # Create server-side cursor (more memory efficient)
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        cursor.execute("SELECT * FROM user_data")
        
        # Stream rows one by one using yield
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
            
    except Error as e:
        print(f"Database error: {e}")
        yield None
    finally:
        # Clean up resources
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()