import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'finance.db')

class DatabaseManager:
    def __init__(self):
        self._create_tables()

    def get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_tables(self):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                # Create Users Table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL
                    )
                """)
                # Create Transactions Table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        type TEXT NOT NULL,  -- 'Income' or 'Expense'
                        category TEXT NOT NULL,
                        amount REAL NOT NULL,
                        date TEXT NOT NULL,
                        description TEXT,
                        FOREIGN KEY (user_id) REFERENCES users (id)
                    )
                """)
                conn.commit()
        except sqlite3.Error as e:
            print(f"Database error during setup: {e}")

    # User operations
    def register_user(self, username, password):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                return True, "Registration successful."
        except sqlite3.IntegrityError:
            return False, "Username already exists."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def authenticate_user(self, username, password):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()
                if user:
                    return True, dict(user)
                return False, "Invalid username or password."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    # Transaction operations
    def add_transaction(self, user_id, t_type, category, amount, date, description):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO transactions (user_id, type, category, amount, date, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (user_id, t_type, category, amount, date, description))
                conn.commit()
                return True, "Transaction added successfully."
        except sqlite3.Error as e:
            return False, f"Database error: {e}"

    def get_transactions(self, user_id):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM transactions WHERE user_id = ? ORDER BY date DESC", (user_id,))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []

    def search_transactions(self, user_id, query):
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                search_term = f"%{query}%"
                cursor.execute("""
                    SELECT * FROM transactions 
                    WHERE user_id = ? AND (
                        category LIKE ? OR
                        description LIKE ? OR
                        type LIKE ? OR
                        date LIKE ?
                    )
                    ORDER BY date DESC
                """, (user_id, search_term, search_term, search_term, search_term))
                return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return []
