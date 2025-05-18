import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="anyhaw"
        )
        if connection.is_connected():
            print("✅ Connected to 'anyhaw' database")
            return connection
    except Error as err:
        print(f"❌ Connection error: {err}")
    return None

