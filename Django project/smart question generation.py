from flask import Flask, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT,
                  email TEXT,
                  password TEXT)''')
    conn.commit()
    conn.close()

init_db()

# ---------------- HOME ----------------
@app.route('/')
def home():
    return redirect('/login')

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "<h3>Passwords do not match!</h3><a href='/register'>Try Again</a>"

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username,email,password) VALUES (?,?,?)",
                  (username, email, password))
        conn.commit()
        conn.close()

        return redirect('/login')

    return '''
    <h2>Register</h2>
    <form method="POST">
        Username:<br>
        <input type="text" name="username" required><br><br>

        Email:<br>
        <input type="email" name="email" required><br><br>

        Password:<br>
        <input type="password" name="password" required><br><br>

        Confirm Password:<br>
        <input type="password" name="confirm_password" required><br><br>

        <button type="submit">Register</button>
    </form>
    <br>
    <a href="/login">Already have account? Login</a>
    '''

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?",
                  (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['username'] = username
            return redirect('/dashboard')
        else:
            return "<h3>Invalid Credentials!</h3><a href='/login'>Try Again</a>"

    return '''
    <h2>Login</h2>
    <form method="POST">
        Username:<br>
        <input type="text" name="username" required><br><br>

        Password:<br>
        <input type="password" name="password" required><br><br>

        <button type="submit">Login</button>
    </form>
    <br>
    <a href="/register">Create new account</a>
    '''

# ---------------- DASHBOARD ----------------
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    return f'''
    <h2>Welcome {session['username']}</h2>

    <h3>Select Quiz Category</h3>

    <a href="/quiz/Academic">Academic</a><br><br>
    <a href="/quiz/Entertainment">Entertainment</a><br><br>
    <a href="/quiz/General Knowledge">General Knowledge</a><br><br>

    <a href="/profile">Profile</a><br>
    <a href="/logout">Logout</a>
    '''

# ---------------- QUIZ ----------------
@app.route('/quiz/<category>')
def quiz(category):
    if 'username' not in session:
        return redirect('/login')

    return f'''
    <h2>{category} Quiz</h2>
    <p>Quiz will start here...</p>

    <a href="/dashboard">Back to Dashboard</a>
    '''

# ---------------- PROFILE ----------------
@app.route('/profile')
def profile():
    if 'username' not in session:
        return redirect('/login')

    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?",
              (session['username'],))
    user = c.fetchone()
    conn.close()

    return f'''
    <h2>User Profile</h2>

    <p><strong>Username:</strong> {user[1]}</p>
    <p><strong>Email:</strong> {user[2]}</p>

    <a href="/dashboard">Back to Dashboard</a>
    '''

# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

# ---------------- RUN ----------------
if __name__ == '__main__':
    app.run(debug=True)
