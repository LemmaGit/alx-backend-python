import mysql.connector
from mysql.connector import Error

def stream_user_ages():
    """Generator that yields user ages one by one"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='ALX_prodev'
        )
        cursor = connection.cursor()
        
        # Stream ages directly from database
        cursor.execute("SELECT age FROM user_data")
        
        while True:  # First loop
            row = cursor.fetchone()
            if row is None:
                break
            yield row[0]  # Yield just the age
            
    except Error as e:
        print(f"Database error: {e}")
        yield None
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """Calculates average age using streaming generator"""
    total = 0
    count = 0
    
    for age in stream_user_ages():  # Second loop
        if age is not None:
            total += age
            count += 1
    
    return total / count if count > 0 else 0

if __name__ == "__main__":
    average_age = calculate_average_age()
    print(f"Average age of users: {average_age:.2f}")