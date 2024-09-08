from flask import Flask, render_template, request, redirect, url_for, flash
from supabase import create_client, Client
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Gunakan kunci rahasia yang aman

# Konfigurasi Supabase
url = "https://kdfowymufhjpzotbowtx.supabase.co"  # Ganti dengan Project URL
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkZm93eW11ZmhqcHpvdGJvd3R4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU3OTY3NTcsImV4cCI6MjA0MTM3Mjc1N30._JBAk3Hk-8qXZJ8SpSXuNoEpVgB8rgQFDw9mhAogfKs"  # Ganti dengan anon key
supabase: Client = create_client(url, key)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            response = supabase.table('users').select('*').eq('username', username).single().execute()
            user = response.data
            if user and user.get('password') == password:
                return redirect(url_for('login_success'))
            else:
                flash("Invalid username or password. Please try again.", 'error')
        except Exception as e:
            flash("An error occurred while trying to log in. Please try again.", 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Cek apakah username sudah ada
            response = supabase.table('users').select('*').eq('username', username).execute()
            existing_user = response.data
            
            if existing_user:
                # Jika username sudah ada, beri tahu pengguna
                flash('Username already exists. Please choose a different username.', 'error')
            else:
                # Simpan data pengguna baru ke Supabase
                insert_response = supabase.table('users').insert({
                    'username': username,
                    'password': password
                }).execute()
                
                # Cek apakah data berhasil disimpan
                if insert_response.data:
                    flash('Your account has been created! You can now log in.', 'success')
                else:
                    flash('An error occurred while creating your account. Please try again.', 'error')
        except Exception as e:
            flash('An error occurred while trying to sign up. Please try again.', 'error')
    
    return render_template('signup.html')

@app.route('/login_success')
def login_success():
    return "Login successful! Welcome to the application."

if __name__ == '__main__':
    app.run(debug=True)
