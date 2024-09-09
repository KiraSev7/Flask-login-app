from flask import Flask, render_template, request, redirect, url_for, flash, session
from supabase import create_client, Client
import os

# Inisialisasi aplikasi Flask
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Kunci rahasia untuk sesi

# Konfigurasi Supabase
url = "https://kdfowymufhjpzotbowtx.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImtkZm93eW11ZmhqcHpvdGJvd3R4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3MjU3OTY3NTcsImV4cCI6MjA0MTM3Mjc1N30._JBAk3Hk-8qXZJ8SpSXuNoEpVgB8rgQFDw9mhAogfKs"
supabase: Client = create_client(url, key)  # Membuat klien Supabase

@app.route('/')
def index():
    # Halaman utama yang menampilkan nama pengguna jika sudah login
    if 'username' in session:
        return render_template('index.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Menangani proses login
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        try:
            # Cek apakah username ada di database
            response = supabase.table('users').select('*').eq('username', username).single().execute()
            user = response.data
            
            # Verifikasi password (password tidak di-hash di sini)
            if user and user.get('password') == password:
                session['username'] = username  # Simpan nama pengguna di sesi
                return redirect(url_for('index'))
            else:
                flash("Invalid username or password. Please try again.", 'error')
        except Exception:
            flash("An error occurred while trying to log in. Please try again.", 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    # Menangani proses pendaftaran
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        token = request.form['token'].strip()
        ip_address = request.remote_addr  # Mendapatkan alamat IP pengguna

        # Validasi input
        if not username or not password or not token:
            flash('Username, password, and token cannot be empty.', 'error')
            return render_template('signup.html')

        # Validasi token
        token_response = supabase.table('tokens').select('token, is_used').eq('token', token).execute()
        token_data = token_response.data

        if not token_data or token_data[0].get('is_used'):
            flash('Invalid or already used token. Please provide a valid token.', 'error')
            return render_template('signup.html')

        # Cek apakah username sudah ada
        user_response = supabase.table('users').select('username').eq('username', username).execute()
        existing_user = user_response.data
        
        if existing_user:
            flash('Username already exists. Please choose a different username.', 'error')
            return render_template('signup.html')

        # Cek apakah alamat IP sudah digunakan
        ip_check_response = supabase.table('users').select('ip_address').eq('ip_address', ip_address).execute()
        existing_ip_user = ip_check_response.data
        
        if existing_ip_user:
            flash('An account has already been created from this IP address.', 'error')
            return render_template('signup.html')

        # Simpan data pengguna baru ke Supabase
        insert_response = supabase.table('users').insert({
            'username': username,
            'password': password,  # Password tidak di-hash di sini
            'ip_address': ip_address,
            'token': token,
            'token_used': True  # Tandai token sebagai sudah digunakan
        }).execute()

        if insert_response.data:
            # Tandai token sebagai sudah digunakan di tabel tokens
            supabase.table('tokens').update({'is_used': True}).eq('token', token).execute()
            flash('Your account has been created! You can now log in.', 'success')
        else:
            flash('An error occurred while creating your account. Please try again.', 'error')
    
    return render_template('signup.html')

@app.route('/login_success')
def login_success():
    # Halaman sukses login
    return "Login successful! Welcome to the application."

@app.route('/logout')
def logout():
    # Menangani proses logout
    session.pop('username', None)  # Hapus nama pengguna dari sesi
    return redirect(url_for('login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Ambil port dari variabel lingkungan, default 5000
    app.run(host='0.0.0.0', port=port, debug=True)  # Jalankan aplikasi Flask
