import os

from dotenv import load_dotenv

load_dotenv()
# Database connection parameters
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")  # Change if using a remote server
DB_PORT = os.getenv("DB_PORT")  # Default PostgreSQL port

import psycopg2


def get_connection():
    """Create and return a PostgreSQL database connection"""
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print("Database connection failed:", e)
        return None


def create_tables():
    """Create the necessary tables in the database"""
    conn = get_connection()
    if not conn:
        return

    try:
        with conn.cursor() as cur:
            # SQL query to create the users table
            create_users_table_query = """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,        -- Auto-incrementing user ID
                name VARCHAR(100) NOT NULL,    -- User's name
                phone_number VARCHAR(20),      -- User's phone number
                telegram_id VARCHAR(50),       -- User's Telegram ID
                birthday DATE                  -- User's birthday
            );
            """

            # SQL query to create the new table with a foreign key
            create_new_table_query = """
            CREATE TABLE IF NOT EXISTS birthday (
                id SERIAL PRIMARY KEY,       -- Auto-incrementing ID
                name VARCHAR(100) NOT NULL,   -- Name field
                date DATE NOT NULL,           -- Date field
                user_id INT,                  -- Foreign key referencing the users table
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE -- Foreign key constraint
            );
            """

            # Execute the queries
            cur.execute(create_users_table_query)
            cur.execute(create_new_table_query)

            # Commit changes
            conn.commit()

            print("Tables created successfully!")
    except Exception as e:
        print("Error creating tables:", e)
    finally:
        conn.close()


create_tables()