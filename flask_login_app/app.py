from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Database configuration
hostname = "exp.h.filess.io"  # Ganti dengan hostname Anda
database = "UserLogin_rockycryif"  # Ganti dengan nama database Anda
port = "3307"  # Ganti dengan port database Anda
db_username = "UserLogin_rockycryif"  # Ganti dengan username database Anda
db_password = "f0f4c9473f3c8f041b68f826788a66782248be0c"  # Ganti dengan password database Anda

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=hostname,
            database=database,
            user=db_username,
            password=db_password,
            port=port
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print("Error while connecting to MySQL", e)
        return None

@app.route('/')
def index():
    connection = get_db_connection()
    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        connection.close()
        return render_template('index.html', users=users)
    else:
        return "Error connecting to the database."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
