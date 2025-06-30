import mysql.connector
from mysql.connector import Error

def stream_users_in_batches(batch_size):
    """Generator that yields batches of users from the database"""
    try:
        # Establish database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',  # Change to your MySQL password
            database='ALX_prodev'
        )
        
        # Create server-side cursor
        cursor = connection.cursor(dictionary=True)
        
        # Execute query
        cursor.execute("SELECT * FROM user_data")
        
        # Fetch rows in batches
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield batch
            
    except Error as e:
        print(f"Database error: {e}")
        yield None
    finally:
        # Clean up resources
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def batch_processing(batch_size):
    """Process batches to filter users over age 25"""
    for batch in stream_users_in_batches(batch_size):
        if batch is None:
            continue
        filtered_users = [user for user in batch if user['age'] > 25]
        yield filtered_users
    return  # Optional to satisfy linters expecting a return

# Example usage
if __name__ == "__main__":
    for filtered_batch in batch_processing(10):  # Process in batches of 10
        for user in filtered_batch:
            print(f"User over 25: {user['name']} (Age: {user['age']})")
