import mysql.connector
from mysql.connector import Error

def paginate_users(page_size, offset):
    """Fetches a specific page of users from the database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='password',
            database='ALX_prodev'
        )
        cursor = connection.cursor(dictionary=True)
        
        query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
        cursor.execute(query, (page_size, offset))
        
        return cursor.fetchall()
        
    except Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def lazy_paginate(page_size):
    """Generator that lazily loads paginated user data"""
    offset = 0
    while True:  # This is the only loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

# Example usage
if __name__ == "__main__":
    # Process 5 users at a time
    for page in lazy_paginate(5):
        print(f"\nPage with {len(page)} users:")
        for user in page:
            print(f"ID: {user['user_id']}, Name: {user['name']}")