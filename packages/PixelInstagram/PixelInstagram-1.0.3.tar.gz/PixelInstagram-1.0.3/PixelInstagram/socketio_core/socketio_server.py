from flask_socketio import SocketIO, emit
from ..http_server import app

socketio_app = SocketIO(app, logger=True, engineio_logger=True)
users = []
messages = []


@socketio_app.on('send message')
def send_message(message):
    print("receive a chat message")
    print(message)
    messages.append(message)
    emit('server response', {'status': 1})


@socketio_app.on('get message')
def get_message(message):
    print(f"client[{message['name']} get message]")
    print("messages:")
    print(messages)
    for i in messages:
        if i["receiver"] == message['name']:
            messages.remove(i)
            print(message)
            emit('message', i)


@socketio_app.on('user login')
def login(message):
    print(f"{message['name']} login")
    emit('server response', {'status': 1})
    emit('new user', {"name": message['name']}, broadcast=True)
    users.append(message['name'])


@socketio_app.on('connect')
def test_connect():
    print("connect")
    emit('server response', {'data': 'Connected'})


@socketio_app.on('disconnect')
def test_disconnect():
    print('Client disconnected')
