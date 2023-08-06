PixelInstagram
====
Our app can help users transfer their photos into ACG pixel-style photos, such that they can 
share ACG pixel-style photos with their friends while chatting.

✨ Our project includes:
------------
- An innovative IOS app for instant messaging and social sharing with photo style 
transfer.
- Socket-based chat server for instant messaging.
- HTTP protocol-based image processing server for image style transfer.
- Deployment of TensorFlow on a GPU server for fast image style transfer.

✨ Install
--------
**pip install**
```shell
$ pip install PixelInstagram
```

**Install from source**
```shell
$ git clone https://gitee.com/wjh1119/pixel-instagram.git
$ cd PixelInstagram
$ pip install -r requirements.txt
$ python setup.py install
```

✨ How to use
---------------
#### 1. photo processing
You can use the following command to start a flask server.
```shell
PI flask -p {port}
```

Then you can use this web api to transfer you photo.

#### 2. chat server (using server)
You can use the following command to start a chat server.
```shell
PI server -p {port}
```

#### 3. chat client(for testing or demo)
You can use the following command to start a chat server.
```shell
PI demo_client -p {server_port} -h {server_host}
```

#### 4. Another socket frame: **Socketio**(we do not use it on our ios app)
- socketio server
```shell
PI socketio_server -p {server_port}
```

- socketio demo client
```shell
PI socketio_server -p {user_port} -n {user_name}
```