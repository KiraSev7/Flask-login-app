from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Dummy user data
USER_DATA = {'username': 'user', 'password': 'pass'}

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USER_DATA['username'] and password == USER_DATA['password']:
            return redirect(url_for('welcome'))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route('/welcome')
def welcome():
    return "Welcome to the protected area!"

if __name__ == '__main__':
    app.run(debug=True)
