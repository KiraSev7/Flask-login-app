from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Database configuration
hostname = "exp.h.filess.io"
database = "UserLogin_rockycryif"
port = "3307"
db_username = "UserLogin_rockycryif"
db_password = "f0f4c9473f3c8f041b68f826788a66782248be0c"

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

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        connection = get_db_connection()
        if connection:
            cursor = connection.cursor()
            query = "SELECT * FROM users WHERE email = %s AND password = %s"
            cursor.execute(query, (email, password))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            
            if user:
                # Jika login berhasil, redirect ke halaman sukses
                return redirect(url_for('login_success'))
            else:
                # Jika login gagal, kembali ke halaman login dengan pesan error
                return render_template('login.html', error="Invalid email or password. Please try again.")
        else:
            # Jika koneksi gagal, tampilkan pesan error umum
            return render_template('login.html', error="Error connecting to the database.")
    
    return render_template('login.html')

@app.route('/login_success')
def login_success():
    return "Login successful! Welcome to the application."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
