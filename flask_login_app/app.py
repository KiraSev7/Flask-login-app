from flask import Flask, render_template, request, redirect, url_for, flash, session
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
    if 'username' in session:
        return render_template('index.html', username=session['username'])
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
                session['username'] = username
                return redirect(url_for('index'))
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
        ip_address = request.remote_addr  # Mendapatkan alamat IP pengguna
        
        try:
            # Cek apakah username sudah ada
            response = supabase.table('users').select('*').eq('username', username).execute()
            existing_user = response.data
            
            if existing_user:
                flash('Username already exists. Please choose a different username.', 'error')
            else:
                # Cek apakah alamat IP sudah digunakan
                ip_check_response = supabase.table('users').select('*').eq('ip_address', ip_address).execute()
                existing_ip_user = ip_check_response.data
                
                if existing_ip_user:
                    flash('An account has already been created from this IP address.', 'error')
                else:
                    # Simpan data pengguna baru ke Supabase
                    insert_response = supabase.table('users').insert({
                        'username': username,
                        'password': password,
                        'ip_address': ip_address
                    }).execute()
                    
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

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
