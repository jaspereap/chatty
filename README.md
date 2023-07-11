# Chatty: Social Application
#### Description:
## Chatty
Chatty is a simple chatting web application that allows users to create chatrooms and engage in real-time conversations. Users can socialize, discuss plans, or communicate with others within the chatrooms.

## Features
- User registration: Users can create an account to access the application.
- Login: Registered users can log in to their accounts.
- Dashboard: Users have access to a dashboard where they can manage their chatrooms and participate in conversations.
- Create Chatrooms: Users can create their own chatrooms and set a description.
- Delete Chatrooms: Users that owns the chatroom can delete the room, along with the messages in it.
- Join Chatrooms: Users can join existing chatrooms and engage in conversations with other participants.
- Real-time Communication: Messages are sent and received in real-time, providing an interactive chatting experience.
- Logout: Users can securely log out from their accounts.
## Technologies Used
Flask: Python web framework used for building the application.

SQLite3: Lightweight relational database used for data storage.

flask-socketio: Flask extension that adds WebSocket support to Flask application, enabling real-time bidirectional communication between client and server.

flask-login: Flask extension used for user authentication and session management

HTML/CSS: Used for structuring and styling the web pages.
Bootstrap: CSS framework for responsive and visually appealing design.

## Walkthrough
### Templates
- In the templates folder, `'layout.html`' serves as the main template that all pages within *Chatty* will extend from. It displays navigation bar items based on whether the user is signed in or not. For instance, an anonymous user will only see 'Register' and 'Login' while a logged in user will see 'Create a room', 'logout', etc. Thanks to flask-login library, a global variable `'current_user'` allows the user to be checked for authentication information.

#### Dashboard
- `'dashboard.html'` provides a summary of all available chatrooms for users to join. This is done by submitting a `GET` response when user visits the page, which calls for the `/dashboard` view route in `app.py`. A database connection is then established to query all the rooms in `rooms.db` and passed back to `dashboard.html` via `render_template`, where each room is iteratively displayed in a table via `Jinja2` for-loop syntax.

#### Chatroom
- When user clicks join, they are redirected to `/chatroom/<int:room_id>` view where the `chatroom.html` template is rendered and served to the user. Message history for that room is also queried from `messages.db` and passed to the client. At the `chatroom.html` page, the script `socket.emit('joinRoom',...)` is called immediately to send a `'joinRoom'` event to the server.
- `@socketio.on('joinRoom')` decorator on the server listens specifically for this event and runs the `joinRoom` function defined under the decorator. This function runs the `join_room` function which is provided by `flask-socketio` library. Joining a room allows targeted message to everyone in the room.
- When users send a message in the chatroom, the event `'group_message'` is emitted to the server, which then replies with the same event name to the client. When the client receives `'group_message'` event, the message is appended to the message box asynchronously. Note that the reply from server is 'targeted' to only the room it received from.
- Using `Jinja2` syntax, the page can also checks if the current user is the owner of the room, because each room stored in `room.db` has an `owner_id` field which is automatically inserted when users create the room. If the user is the owner, they have the option to delete the room, while in the chatroom.

## Installation
Clone the repository:
```bash
git clone https://github.com/your-username/chatty.git
```
Create a virtual environment:
```bash
cd chatty
python -m venv venv
```
Activate the virtual environment:
For Windows:
```
venv\Scripts\activate
For macOS/Linux:
```
```bash
source venv/bin/activate
Install the required dependencies:
pip install -r requirements.txt
```
Run the application:
```python
python app.py
```
Access the application in your web browser at http://localhost:5000.

## Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to submit a pull request.

## Acknowledgements
[Flask](https://flask.palletsprojects.com/en/2.3.x/): The web framework used for building the application.

[SQLite](https://www.sqlite.org/index.html): The lightweight database used for data storage.

[Socket.IO](https://socket.io/): The real-time communication library used for enabling real-time messaging.

[Bootstrap](https://getbootstrap.com/): The CSS framework used for styling the application.

## Contact
For any questions or inquiries, please contact jaspereap@gmail.com
