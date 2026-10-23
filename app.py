from flask import Flask, request
import sqlite3
app = Flask(__name__)
DATABASE = "registrations.db"
MAX_PARTICIPANTS = 50
def create_table():
    connection = sqlite3.connect(DATABASE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            college TEXT,
            department TEXT,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    connection.commit()
    connection.close()
def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection
@app.route("/")
def home():
    return {"message": "Event Registration Backend is running!"}
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return {"error": "Please send registration details as JSON"}, 400
    name = data.get("name", "")
    email = data.get("email", "")
    if not isinstance(name, str) or not isinstance(email, str):
        return {"error": "Name and email must be text"}, 400
    name = name.strip()
    email = email.strip()
    if not name or not email:
        return {"error": "Name and email are required"}, 400
    if "@" not in email or "." not in email.split("@")[-1]:
        return {"error": "Please enter a valid email address"}, 400
    college = data.get("college", "")
    department = data.get("department", "")
    if not isinstance(college, str) or not isinstance(department, str):
        return {"error": "College and department must be text"}, 400
    connection = get_connection()
    try:
        count = connection.execute(
            "SELECT COUNT(*) FROM registrations"
        ).fetchone()[0]
        if count >= MAX_PARTICIPANTS:
            return {
                "error": f"Registration is full. Maximum {MAX_PARTICIPANTS} participants allowed."
            }, 409
        connection.execute(
            """
            INSERT INTO registrations (name, email, college, department)
            VALUES (?, ?, ?, ?)
            """,
            (name, email, college.strip(), department.strip())
        )
        connection.commit()
        student = connection.execute(
            "SELECT * FROM registrations WHERE email = ?",
            (email,)
        ).fetchone()
        return {
            "message": "Registration successful!",
            "registration": dict(student)
        }, 201
    except sqlite3.IntegrityError:
        return {"error": "This email is already registered"}, 409
    finally:
        connection.close()
@app.route("/registrations", methods=["GET"])
def get_registrations():
    connection = get_connection()
    email = request.args.get("email")
    if email:
        student = connection.execute(
            "SELECT * FROM registrations WHERE email = ?",
            (email.strip(),)
        ).fetchone()
        connection.close()
        if student is None:
            return {"error": "Registration not found"}, 404
        return {"registration": dict(student)}, 200
    students = connection.execute(
        "SELECT * FROM registrations ORDER BY id"
    ).fetchall()
    connection.close()
    return {
        "total": len(students),
        "registrations": [dict(student) for student in students]
    }, 200
@app.route("/registrations/<int:registration_id>", methods=["GET"])
def get_registration_by_id(registration_id):
    connection = get_connection()
    student = connection.execute(
        "SELECT * FROM registrations WHERE id = ?",
        (registration_id,)
    ).fetchone()
    connection.close()
    if student is None:
        return {"error": "Registration not found"}, 404
    return {"registration": dict(student)}, 200
if __name__ == "__main__":
    create_table()
    app.run(debug=True)