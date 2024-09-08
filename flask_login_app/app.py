from flask import Flask, send_from_directory, request, redirect, url_for
import os

app = Flask(__name__)

@app.route('/')
def index():
    return send_from_directory('', 'login.html')

@app.route('/welcome')
def welcome():
    return "Welcome to the protected area!"

if __name__ == '__main__':
    # Get the PORT from the environment variable or default to 5000
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
