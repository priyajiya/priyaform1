from flask import Flask, request, render_template, redirect, url_for
import mysql.connector

# Initialize the Flask app
app = Flask(__name__, template_folder="templates")

# Database connection details
DB_HOST = 'mysql'  # Container name in docker-compose
DB_USER = 'root'
DB_PASSWORD = 'password'
DB_NAME = 'registration_db'

# Connect to MySQL database
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

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

