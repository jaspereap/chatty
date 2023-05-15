from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['DATABASE'] = 'users.db'
# For unit testing
# app.config['LOGIN_DISABLED'] = False

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login' # name of function to login page
login_manager.login_message = 'Please log in first.'
@login_manager.user_loader
def load_user(user_id):
    db = get_db()
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(id=user['id'], username=user['username'], password=user['password'])
    else:
        return None

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

def get_db():
    """Get the database connection for the current thread."""
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(error):
    """Close the database connection at the end of a request."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=['POST','GET'])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # Else if user submitted the form
    # Get user input
    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Check if username in db and is valid
    db = get_db()
    username_db = db.execute('SELECT * FROM users')
    for row in username_db:
        row = dict(row)['username']
        if username == row:
            flash("Username already exists")
            return render_template("register.html")

    # Check if password matches and is valid
    if password != confirm_password or len(password) < 4 or len(password) > 20:
        flash("Please enter your password again")
        return render_template("register.html")

    # Add user into db if both valid
    db = get_db()
    cursor = db.cursor()
    password = generate_password_hash(password)
    try:
        cursor.execute('INSERT INTO users (username,password) VALUES (?,?)',(username,password))
        db.commit()
        flash('Registration successful!')
        return redirect(url_for('index'))
    except:
        flash("Error adding user to database")
        return render_template("register.html")

@app.route("/login", methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    # Else get user input
    username = request.form.get('username')
    password = request.form.get('password')
    db = get_db()
    userdb = db.execute('SELECT * FROM users')
    for row in userdb:
        row = dict(row)
        print(row)
        if row['username'] == username:
            if check_password_hash(row['password'], password):
                id = row['id']
                login_user(User(id=id, username=username, password=password))
                flash('Successfully logged in')
                return redirect(url_for('dashboard'))
    flash('Incorrect username or password! Please check your username and password.')
    return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged out, goodbye')
    return redirect('login')

@app.route("/dashboard", methods=['POST','GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)