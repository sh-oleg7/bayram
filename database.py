import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# Database connection parameters
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")  # Change if using a remote server
DB_PORT = os.getenv("DB_PORT")  # Default PostgreSQL port


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


def get_user_id_by_telegram(telegram_id):
    """Get the user_id by the user's telegram_id"""
    conn = get_connection()
    if conn is None:
        return None

    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM users WHERE telegram_id = %s;", (telegram_id,))
        user_id = cur.fetchone()
        return user_id[0] if user_id else None
    except Exception as e:
        print("Error fetching user ID:", e)
        return None
    finally:
        cur.close()
        conn.close()


def create_user(name, phone_number, telegram_id, birthday):
    """Insert a new user into the users table."""
    conn = get_connection()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, phone_number, telegram_id, birthday) "
            "VALUES (%s, %s, %s, %s) RETURNING id;",
            (name, phone_number, telegram_id, birthday)
        )
        user_id = cur.fetchone()[0]  # Get the inserted user's ID
        conn.commit()
        print(f"User created successfully with ID {user_id}")
        return user_id
    except Exception as e:
        print("Error inserting user:", e)
    finally:
        cur.close()
        conn.close()


def create_birthday_data(name, date, telegram_id):
    """Insert a new record into the new_table, using telegram_id"""
    user_id = get_user_id_by_telegram(telegram_id)

    # If user doesn't exist, create a new one
    # if not user_id:
    #     print(f"User with telegram_id {telegram_id} not found. Creating new user...")
    #     # Example of creating a new user
    #     user_id = create_user(name="New User", phone_number="0000000000", telegram_id=telegram_id,
    #                           birthday="2000-01-01")

    if user_id:
        conn = get_connection()
        if conn is None:
            return

        try:
            cur = conn.cursor()

            # Print attempt details
            print(f"Attempting to insert: name={name}, date={date}, user_id={user_id}")

            cur.execute(
                "INSERT INTO birthday (name, date, user_id) "
                "VALUES (%s, %s, %s) RETURNING id;",
                (name, date, user_id)
            )
            record_id = cur.fetchone()  # Get the inserted record's ID

            if record_id:
                print(f"Record created successfully with ID {record_id[0]}")
            else:
                print("Failed to get record ID after insertion.")

            conn.commit()  # Commit changes
        except Exception as e:
            print(f"Error inserting record into new_table: {e}")
        finally:
            cur.close()
            conn.close()

#
# create_user(
#     name="John Doe",
#     phone_number="1234567890",
#     telegram_id="123456",
#     birthday="1990-05-15"  # Example birthday date
# )
#
#
#
# create_birthday_data(
#     name="John's Birthday",
#     date="2025-02-04",  # Пример даты
#     telegram_id="123456"  # Пример Telegram ID
# )
