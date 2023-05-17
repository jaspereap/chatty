# Chatty: Social Application
#### Video Demo:  <URL HERE>
#### Description:
## Chatty
Chatty is a simple chatting web application that allows users to create chatrooms and engage in real-time conversations. Users can socialize, discuss plans, or communicate with others within the chatrooms.

## Features
User registration: Users can create an account to access the application.
Login: Registered users can log in to their accounts.
Dashboard: Users have access to a dashboard where they can manage their chatrooms and participate in conversations.
Create Chatrooms: Users can create their own chatrooms and set a description.
Join Chatrooms: Users can join existing chatrooms and engage in conversations with other participants.
Real-time Communication: Messages are sent and received in real-time, providing an interactive chatting experience.
Logout: Users can securely log out from their accounts.
## Technologies Used
Flask: Python web framework used for building the application.
SQLite3: Lightweight relational database used for data storage.
Socket.IO: Real-time event-based communication library for enabling real-time messaging in the chatrooms.
HTML/CSS: Used for structuring and styling the web pages.
Bootstrap: CSS framework for responsive and visually appealing design.
## Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/chatty.git
Create a virtual environment:
bash
Copy code
cd chatty
python -m venv venv
Activate the virtual environment:
For Windows:
Copy code
venv\Scripts\activate
For macOS/Linux:
bash
Copy code
source venv/bin/activate
Install the required dependencies:
Copy code
pip install -r requirements.txt
Run the application:
Copy code
python app.py
Access the application in your web browser at http://localhost:5000.
## Configuration
Database: By default, the application uses an SQLite database file (chatty.db) stored in the project's root directory. If you need to change the database settings, update the app.config['DATABASE'] configuration in app.py.
## Contributing
Contributions are welcome! If you have any suggestions, improvements, or bug fixes, feel free to submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
[Flask](https://flask.palletsprojects.com/en/2.3.x/): The web framework used for building the application.
[SQLite](https://www.sqlite.org/index.html): The lightweight database used for data storage.
[Socket.IO](https://socket.io/): The real-time communication library used for enabling real-time messaging.
[Bootstrap](https://getbootstrap.com/): The CSS framework used for styling the application.
## Contact
For any questions or inquiries, please contact jaspereap@gmail.com
