from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample username and password for login
USERNAME = 'admin'
PASSWORD = 'password'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == USERNAME and password == PASSWORD:
            return "Login successful!"
        else:
            return "Invalid credentials. Please try again."
    return render_template('login.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
