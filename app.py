import hashlib
from http import client
import sqlite3
from flask import send_file
import os
import sqlite3
import secrets
from flask import Flask, jsonify, request, session,g,send_file
from itsdangerous import URLSafeSerializer
from flask import Flask, request, render_template_string
from flask_mail import Mail, Message

app = Flask(__name__)
conn = sqlite3.connect('new.db')
cursor = conn.cursor()
app.secret_key = secrets.token_urlsafe(32)

# create db
import sqlite3

def init_db():
    conn = sqlite3.connect('new.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                verified INTEGER DEFAULT 0       
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                clients TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                verified INTEGER DEFAULT 0         
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS uploads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_name TEXT UNIQUE NOT NULL,
                file_data BLOB NOT NULL
            )
        ''')
        
        cursor.execute("PRAGMA table_info(uploads)")
        columns = cursor.fetchall()
        verified_column_exists = any(column[1] == 'verified' for column in columns)
        
        if not verified_column_exists:
            cursor.execute('ALTER TABLE uploads ADD COLUMN file_data BLOB NOT NULL')
        
        conn.commit()
        print("Tables created successfully.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


init_db()




# Admin login route
@app.route('/admin-login', methods=['POST'])
def admin_login():
    data = request.json  
    username = data.get('username')
    password = data.get('password')

    
    if username == 'admin' and password == 'admin_password':
        session['admin'] = True 
        return 'Admin login successful', 200
    else:
        return 'Invalid credentials', 401

# # File upload route for admin
@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'admin' in session and session['admin']:
        file = request.files['file']
        if file.filename.endswith(('pptx', '.docx', '.xlsx')):
            
            return 'File uploaded successfully', 200
        else:
            return 'File type not allowed', 400
    else:
        return 'Unauthorized', 403
    
# Logout route for admin
@app.route('/client-signout', methods=['GET'])
def client_signout():
        session.pop('username', None)
        return 'User logged out', 200


import sqlite3

def add_file_data_column():
    conn = sqlite3.connect('new.db')
    cursor = conn.cursor()
    
    try:
        
        cursor.execute("SELECT file_data FROM uploads")
        cursor.fetchone()  
         
        print("Column 'file_data' already exists in the table 'uploads'")
    except sqlite3.OperationalError:
       
        cursor.execute("ALTER TABLE uploads ADD COLUMN file_data BLOB NOT NULL")
        conn.commit()
        print("Column 'file_data' added to the table 'uploads'")
    finally:
        conn.close()


add_file_data_column()

app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = '87dc4001dcb3b3'
app.config['MAIL_PASSWORD'] = '5f6a3a15645fa3'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('new.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/email-verify/<username>')
def email_verify(username):
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE users SET verified=1 WHERE username=?", (username,))
        db.commit()
        cursor.close()
        return f"Email verified for user {username}"
    except sqlite3.Error as e:
        return f"Error: {e}"
    
#client signup

@app.route('/client-signup', methods=['POST'])
def client_signup():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')

  
    if not username or not email or not password:
        return 'Username, email, and password are required', 400
    
    conn = sqlite3.connect('new.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE username=? OR email=?", (username, email))
    existing_user = cursor.fetchone()

    if existing_user:
        return 'Username or email already exists', 409

   
    hashed_password = hashlib.sha256(password.encode()).hexdigest()  # Hashing the password
    cursor.execute("INSERT INTO clients (username, email, password) VALUES (?, ?, ?)", (username, email, hashed_password))
    conn.commit()
    conn.close()

    # Generate an email verification link
    verification_link = f"http://127.0.0.1:5000/email-verify/{username}"


    return f'Email verification link sent for {username}: {verification_link}', 200

@app.route('/client-signin', methods=['POST'])
def client_signin():
    username = request.json.get('username')
    password = request.json.get('password')

  
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clients WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
       
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if hashed_password == user[3]:  # Assuming password is stored in the fourth column
            return jsonify({'message': 'Sign in successful'}), 200
        else:
            return jsonify({'error': 'Invalid password'}), 401
    else:
        return jsonify({'error': 'User not found'}), 404
    

@app.route('/download/<username>/<file_name>', methods=['GET'])
def download_file(username, file_name):
    
    if username in client:
        # Fetch the db
        conn = sqlite3.connect('new.db')  
        cursor = conn.cursor()

        cursor.execute("SELECT file_data FROM uploads WHERE admin_user_id = ? AND file_name = ?", (username, file_name))
        file_data = cursor.fetchone()

        print(file_data)  

        if file_data:
            
            return send_file(file_data[0], as_attachment=True), 200
        else:
            return jsonify({'error': 'File not found'}), 404
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/signout', methods=['GET'])
def signout():
    if 'username' in session:
        session.pop('username', None)
        return 'Sign out successful', 200
    else:
        return 'No user signed in', 401

if __name__ == '__main__':
    app.secret_key = secrets.token_urlsafe(32)
    app.run(debug=True)

