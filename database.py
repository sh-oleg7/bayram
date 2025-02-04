import psycopg2

# Database connection parameters
DB_NAME = "bayramtest"
DB_USER = "postgres"
DB_PASSWORD = "1688835oleg"
DB_HOST = "localhost"  # Change if using a remote server
DB_PORT = "5432"  # Default PostgreSQL port

# Establish connection
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()

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
    CREATE TABLE IF NOT EXISTS new_table (
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
    print("Error:", e)

finally:
    # Close the cursor and connection
    if cur:
        cur.close()
    if conn:
        conn.close()


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
    except Exception as e:
        print("Error inserting user:", e)
    finally:
        cur.close()
        conn.close()


def create_new_record(name, date, user_id):
    """Insert a new record into the new_table."""
    conn = get_connection()
    if conn is None:
        print("Connection failed")
        return

    try:
        cur = conn.cursor()

        # Проверим, что передаваемые данные валидны
        print(f"Attempting to insert: name={name}, date={date}, user_id={user_id}")

        cur.execute(
            "INSERT INTO new_table (name, date, user_id) "
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


def create(holiday_name, holiday_date_str, user_id):
    """Функция для создания записи в таблице."""
    # Проверяем, что holiday_name и holiday_date_str не пустые
    if not holiday_name or not holiday_date_str:
        print("Ошибка: имя праздника или дата не указаны.")
        return None

    # Вставляем данные в таблицу через create_new_record
    create_new_record(holiday_name, holiday_date_str, user_id)

    # Если вставка успешна, возвращаем сообщение об успешной вставке
    return f"Праздник {holiday_name} успешно добавлен на {holiday_date_str}."
