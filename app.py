from flask import Flask, render_template, request, redirect, url_for, flash, session, g 
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
app.config['DATABASE'] = 'users.db'
# For unit testing
# app.config['LOGIN_DISABLED'] = False
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login' # name of function to login page
login_manager.login_message = 'Please log in first.'

@login_manager.user_loader
def load_user(user_id):
    db = get_db(app.config['DATABASE'])
    user = db.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    if user:
        return User(id=user['id'], username=user['username'], password=user['password'])
    else:
        return None

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = int(id)
        self.username = username
        self.password = password

def get_db(db_name):
    """Get the database connection for the specified database name."""
    if 'dbs' not in g:
        g.dbs = {}  # Store database connections in a dictionary
    if db_name not in g.dbs:
        g.dbs[db_name] = sqlite3.connect(db_name)
        g.dbs[db_name].row_factory = sqlite3.Row
    return g.dbs[db_name]


@app.teardown_appcontext
def close_db(error):
    """Close the database connections at the end of a request."""
    dbs = getattr(g, 'dbs', {})
    for db_name, db_conn in dbs.items():
        db_conn.close()
    g.dbs = {}


# SocketIO
@socketio.on('systemMessage')
def systemMessage(message):
    print("Server message: "+ message)

@socketio.on('disconnect')
def disconnect():
    print(current_user.username + " has disconnected")

@socketio.on('redirect_room')
def redirect_room(data):
    room_id = data['room_id']
    room_name = data['room_name']
    username = data['username']
    return render_template('chatroom.html', room_id=room_id,room_name=room_name)

@socketio.on('joinRoom')
def joinRoom(data):
    room_id = data['room_id']
    room_name = data['room_name']
    username = data['username']
    print(f"{username} joins room {room_name}, with room id: {room_id}")
    join_room(room_id)
    emit('clientMessage',f"{username} has joined {room_name}.",to=room_id)

@socketio.on('groupMessage')
def groupMessage(data):
    username = data['username']
    message = data['message']
    room_id = data['room_id']
    date = datetime.datetime.now().strftime("%H:%M:%S")
    emit('group_message',{'username':username,'message':message,'date':date},to=room_id)

# Flask Routing
@app.route("/")
def index():
    return render_template("index.html")

@app.route('/chatroom/<string:room_id>')
@login_required
def redirect_chatroom(room_id):
    room_name = ''
    owner = ''
    db = get_db('rooms.db')
    rooms_db = db.execute('SELECT * FROM rooms')
    for room in rooms_db:
        if room['room_id'] == int(room_id):
            room_name = room['room_name']
            owner = int(room['owner'])
    return render_template('chatroom.html',room_id=room_id,room_name=room_name,owner=owner)

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
    db = get_db(app.config['DATABASE'])
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
    db = get_db(app.config['DATABASE'])
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
    db = get_db(app.config['DATABASE'])
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
    db = get_db('rooms.db')
    rooms_db = db.execute('SELECT * FROM rooms')
    rooms = []
    for row in rooms_db:
        room = dict(row)
        rooms.append(room)
    return render_template('dashboard.html', rooms=rooms)

@app.route("/new_room", methods=['POST','GET'])
def new_room():
    if request.method == 'GET':
        return render_template('new_room.html')
    # Get user input
    room_name = request.form.get('room_name')
    room_desc = request.form.get('room_desc')
    user_id = current_user.get_id()
    # Get room database
    db = get_db('rooms.db')
    db.execute('INSERT INTO rooms (room_name, room_desc, owner) VALUES (?, ?, ?)', (room_name, room_desc, user_id))
    db.commit()
    flash('New room has been created successfully!')
    return redirect(url_for('dashboard'))

@app.route("/delete_room", methods=['POST'])
def delete_room():
    room_id = request.form.get('room_id')
    owner = request.form.get('owner')
    db = get_db('rooms.db')
    rooms_db = db.execute('SELECT * FROM rooms')
    for row in rooms_db:
        print(row['room_id'])
        print(row['owner'])
        if row['room_id'] == int(room_id):
            if row['owner'] == int(owner):
                print("DELETE FROM DATABASE")
                db.execute('DELETE FROM rooms WHERE room_id = ? AND owner = ?', (room_id, int(owner)))
                db.commit()
                return redirect(url_for('dashboard'))
    flash('You are not the owner')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    socketio.run(app)