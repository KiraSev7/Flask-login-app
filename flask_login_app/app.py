from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Dummy user data
USER_DATA = {'username': 'user', 'password': 'pass'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USER_DATA['username'] and password == USER_DATA['password']:
            # Jika login berhasil, redirect ke halaman sukses
            return redirect(url_for('login_success'))
        else:
            # Jika login gagal, kembali ke halaman login dengan pesan error
            return render_template('login.html', error="Invalid username or password. Please try again.")
    
    return render_template('login.html')

@app.route('/login_success')
def login_success():
    return "Login successful! Welcome to the application."

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
