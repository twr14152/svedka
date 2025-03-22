from flask import Flask, request, redirect, render_template, session, g, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Initialize the Flask app
app = Flask(__name__)
app.secret_key = '#########'

# SQLite database location
DATABASE = 'users.db'

# Database connection helper
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row  # Enables accessing rows as dictionaries
    return g.db

@app.teardown_appcontext
def close_db(exception=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Create the users table (run this once)
def init_db():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT 0
    )''')
    db.commit()

    # Ensure an admin account exists
    admin_exists = db.execute("SELECT 1 FROM users WHERE is_admin = 1").fetchone()
    if not admin_exists:
        hashed_password = generate_password_hash('###')  # Default admin password
        db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                   ('admin', hashed_password, 1))
        db.commit()
        print("Admin account created with username: 'admin' and password: '###'.")

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')  # If logged in, redirect to the dashboard
    return render_template('index.html')  # Otherwise, show the index page

@app.route('/logout')
def logout():
    session.pop('user_id', None)  # Removes the user_id from the session
    return redirect('/login')  # Redirect to the login page

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' not in session:
        return redirect('/login')  # If logged in, redirect to the dashboard
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)  # Hash the password
        try:
            db = get_db()
            db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                       (username, hashed_password, 0))  # Default: non-admin user
            db.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already exists."
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if user:
            print(f"User fetched: {user['username']}")
        if user and check_password_hash(user['password'], password):  # Verify the password
            session['user_id'] = user['id']
            print(f"User authenticated: {username}")
            return redirect('/admin') if user['is_admin'] else redirect('/dashboard')
        return "Invalid credentials."
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')  # Ensure the user is logged in

    db = get_db()
    user = db.execute("SELECT username FROM users WHERE id = ?", (session['user_id'],)).fetchone()

    if not user:
        return "User not found.", 404  # Handle cases where the user doesn't exist

    username = user['username']  # Extract the username
    return render_template('dashboard.html', username=username)


@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'user_id' not in session:
        return redirect('/login')  # Ensure the user is logged in

    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()

        # Verify the old password and update to the new password
        if user and check_password_hash(user['password'], old_password):
            hashed_new_password = generate_password_hash(new_password)
            db.execute("UPDATE users SET password = ? WHERE id = ?", (hashed_new_password, session['user_id']))
            db.commit()
            return "Password successfully changed!"
        else:
            return "Invalid old password."

    return render_template('change_password.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    # Ensure only admins can access this route
    if 'user_id' not in session:
        return redirect('/login')
    db = get_db()
    user = db.execute("SELECT * FROM users WHERE id = ?", (session['user_id'],)).fetchone()
    if not user or user['is_admin'] == 0:
        return "Access denied. Admins only."

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            username = request.form['username']
            password = request.form['password']
            hashed_password = generate_password_hash(password)  # Hash the password
            try:
                db.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                           (username, hashed_password, 0))
                db.commit()
            except sqlite3.IntegrityError:
                return "Username already exists."
        elif action == 'remove':
            user_id = request.form['user_id']
            db.execute("DELETE FROM users WHERE id = ?", (user_id,))
            db.commit()

    # Fetch all users
    users = db.execute("SELECT * FROM users").fetchall()
    return render_template('admin.html', users=users)

############# Auth/admin code above this line ####################



@app.route('/fill_form', methods=['GET', 'POST'])
def fill_form():
    if 'user_id' not in session:
        return redirect('/login')  # Ensure the user is logged in

    if request.method == 'POST':
        form_data = request.form['form_data']  # Replace 'form_data' with your actual form fields
        # Process the form data (e.g., save it to the database)
        return redirect('/dashboard')

    return render_template('form.html')

@app.route('/generate_quote', methods=['GET', 'POST'])
def generate_quote():
    if 'form_data' not in session:  # Ensure there’s data saved in the session
        return redirect('/fill_form')  # Redirect back to fill_form if no data exists

    if request.method == 'POST':
        # Access the initial data and new input
        initial_data = session['form_data']  # Retrieve the previous form data
        new_input = request.form['additional_data']

        # Perform the desired computation
        computed_result = f"Processed: {initial_data} and {new_input}"  # Example computation
        return f"Quote generated based on your input: {computed_result}"

    # Display the form to gather additional data
    return render_template('generate_quote.html', initial_data=session['form_data'])


### App code above this line ####

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Initialize the database
    app.run(debug=True)
