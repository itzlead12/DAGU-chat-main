from flask import Flask, request, session, redirect, render_template, g
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
DATABASE = 'chat_app.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        last_online DATETIME
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sender_id INTEGER NOT NULL,
        receiver_id INTEGER NOT NULL,
        message_text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (sender_id) REFERENCES users(id),
        FOREIGN KEY (receiver_id) REFERENCES users(id)
    )
    """)
    db.commit()

def create_user(username, email, password_hash):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                   (username, email, password_hash))
    db.commit()

def get_user_by_username(username):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    return cursor.fetchone()

def send_message(sender_id, receiver_id, message_text):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO messages (sender_id, receiver_id, message_text) VALUES (?, ?, ?)",
                   (sender_id, receiver_id, message_text))
    db.commit()

def get_messages(user1_id, user2_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT m.message_text, u.username AS sender
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE (m.sender_id=? AND m.receiver_id=?) OR (m.sender_id=? AND m.receiver_id=?)
        ORDER BY m.timestamp
    """, (user1_id, user2_id, user2_id, user1_id))
    return cursor.fetchall()

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        try:
            create_user(username, email, password)
            return "User registered successfully!"
        except sqlite3.IntegrityError:
            return "Username or email already exists."
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = get_user_by_username(username)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect('/chat')
        else:
            return "Invalid username or password."
    return render_template('login.html')

    
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        receiver_username = request.form['receiver']
        message = request.form['message']

        encrypted_message = message  

        cursor.execute("SELECT id FROM users WHERE username=?", (receiver_username,))
        receiver = cursor.fetchone()
        if receiver:
            send_message(session['user_id'], receiver['id'], encrypted_message)
        else:
            return "Receiver not found."

    cursor.execute("""
        SELECT m.message_text, u.username AS sender
        FROM messages m
        JOIN users u ON m.sender_id = u.id
        WHERE m.sender_id=? OR m.receiver_id=?
        ORDER BY m.timestamp
    """, (session['user_id'], session['user_id']))
    messages = cursor.fetchall()

    return render_template('chat.html', messages=messages)

if __name__ == '__main__':
    with app.app_context():
        init_db() 
    app.run(debug=True, port=5050)
