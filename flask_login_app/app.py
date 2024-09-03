from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Database configuration
hostname = "exp.h.filess.io"
database = "UserLogin_rockycryif"
port = "3307"
username_db = "UserLogin_rockycryif"
password_db = "f0f4c9473f3c8f041b68f826788a66782248be0c"

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=username_db,
            password=password_db,
            port=port
        )
        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)
    except Error as e:
        print("Error while connecting to MySQL", e)
    return connection

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Create a connection to the database
        connection = create_db_connection()
        if connection:
            cursor = connection.cursor()

            # Query to check user credentials
            cursor.execute("SELECT * FROM users WHERE email=%s AND password=%s", (email, password))
            user = cursor.fetchone()

            cursor.close()
            connection.close()

            if user:
                return "Login successful!"
            else:
                return "Invalid credentials. Please try again."
        else:
            return "Failed to connect to the database."

    return render_template('login.html')

if __name__ == '__main__':
    # Use Railway-provided PORT or default to 5000
    port = int(os.getenv("PORT", default=5000))
    app.run(host='0.0.0.0', port=port)
