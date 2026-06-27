import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('students.db')
        self.cursor = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            coffee INTEGER DEFAULT 0,
            motivation INTEGER DEFAULT 100,
            bugs INTEGER DEFAULT 5,
            xp INTEGER DEFAULT 0,
            level INTEGER DEFAULT 1,
            salary INTEGER DEFAULT 400
        )
        """)

    def register_user(self, username, password, role):
        try:
            self.cursor.execute(
                """
                INSERT INTO users (username, password, role)
                VALUES (?, ?, ?)
                """,
                (username, password, role)
            )
            self.conn.commit()
            return True
        except:
            return False

    def login_user(self, username, password):
        self.cursor.execute(
            """
            SELECT * FROM users
            WHERE username=? and password=?
            """,
            (username, password)
        )

        return self.cursor.fetchone()

    def add_student(self, name):
        self.cursor.execute(
            """
            INSERT INTO students(name)
            VALUES (?)
            """,
            (name)
        )
        self.conn.commit()

    def get_students(self):
        self.cursor.execute(
            """
            SELECT * FROM students
            """
        )
        return self.cursor.fetchall()

    def search_student(self, name):
        self.cursor.execute(
            """
            SELECT * FROM students
            WHERE name LIKE ?
            """,
            (f"%{name}%")
        )

    def delete_student(self, student_id):
        self.cursor.execute(
            """
            DELETE FROM students
            WHERE id = ?
            """,
            (student_id,)
        )
        self.conn.commit()

    def update_student(self, student_id, field, value):
        self.cursor.execute(
            f"""
            UPDATE students
            SET {field} = ?
            WHERE id = ?
            """,
            (value, student_id)
        )
        self.conn.commit()

    def get_student(self, student_id):
        self.cursor.execute(
            """
            SELECT * FROM students
            WHERE id = ?
            """,
            (student_id,)
        )
        return self.cursor.fetchone()