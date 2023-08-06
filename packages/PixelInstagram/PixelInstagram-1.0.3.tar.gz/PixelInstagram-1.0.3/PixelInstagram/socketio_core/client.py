from threading import Timer, Event, Thread

import socketio

# standard Python
sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event
def message(data):
    print('I received a message!')

@sio.on('message')
def on_message(data):

    print('I received a message!')
    print(data)


@sio.on('new user')
def on_message(data):
    print(f"new user: {data['name']}")
    print('I received a message!')


@sio.on('server response')
def on_message(data):
    print(data)
    print('I received a message!')


@sio.event
def connect():
    print("I'm connected!")

@sio.event
def connect_error():
    print("The connection failed!")

@sio.event
def disconnect():
    print("I'm disconnected!")


class HeartbeatThread(Thread):
    """心跳"""

    def __init__(self, event, sio, my_name):
        super(HeartbeatThread, self).__init__()
        self.event = event
        self.sio = sio
        self.my_name = my_name

    def run(self):
        while 1:
            # 发送ping包
            self.sio.emit('get message', {'name': self.my_name})
            self.event.wait(timeout=2)

def on_emit(sio, my_name):
    # 创建心跳线程
    event = Event()
    heartbeat = HeartbeatThread(event, sio, my_name)
    heartbeat.start()

    while 1:
        inp = input("input: receiver,content")
        receiver, content = inp.split(",")
        # 发送信息
        # 4: engine.io message
        # 2: socket.io event
        # chat message event message
        sio.emit('send message', {'sender': my_name, 'receiver': receiver, "content": content})
        sio.sleep(.2)


def socketio_client(my_name, port):

    sio.connect(f'http://localhost:{port}')
    sio.emit('user login', {"name": my_name})

    t = Timer(3, on_emit, args=(sio, my_name))
    t.start()
