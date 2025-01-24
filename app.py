from flask import Flask, request, render_template
import mysql.connector
import os
import time

app = Flask(__name__, template_folder="templates")

# Fetch database connection details from environment variables
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'registration_db')

def get_db_connection():
    retries = 5
    while retries > 0:
        try:
            conn = mysql.connector.connect(
                host=DB_HOST,
                user=DB_USER,
                password=DB_PASSWORD,
                database=DB_NAME
            )
            return conn
        except mysql.connector.Error as err:
            print(f"Database connection failed: {err}. Retrying in 5 seconds...")
            time.sleep(5)
            retries -= 1
    raise Exception("Database connection could not be established after retries.")

@app.route("/", methods=["GET", "POST"])
def register():
    success_message = None
    error_message = None

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        course = request.form.get("course")

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INT AUTO_INCREMENT PRIMARY KEY,
                                name VARCHAR(255),
                                age INT,
                                gender VARCHAR(50),
                                course VARCHAR(50))''')
            cursor.execute('INSERT INTO users (name, age, gender, course) VALUES (%s, %s, %s, %s)',
                           (name, age, gender, course))
            conn.commit()
            conn.close()
            success_message = "Registration Successful!"
        except Exception as e:
            error_message = f"Error: {e}"

    return render_template("index.html", success_message=success_message, error_message=error_message)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

