from .yuchunlib import process
from PIL import Image
from .http_server import app
from .socketio_core.socketio_server import socketio_app
from .socketio_core.client import socketio_client
from .demo_client import run_client
from .socket_server import run_server

import click

miner_name = None


@click.group()
def cli():
    pass


@cli.command(name="debug")
def debug():
    img = process_img(Image.open('./chicago.jpg'))
    img.show()


@cli.command(name="flask")
@click.option("-p", "--port")
def flask(port=10155):
    app.run(port=port)


@cli.command(name="demo_client")
@click.option("-h", "--host")
@click.option("-p", "--port")
def socket_client(host, port=10155):
    run_client(host=host, port=int(port))


@cli.command(name="demo_client")
@click.option("-h", "--host")
@click.option("-p", "--port")
def socket_server(host, port=10155):
    run_server(host=host, port=int(port))


@cli.command(name="socketio_server")
@click.option("-p", "--port")
def socketio(port=10155):
    socketio_app.run(app, port=int(port))


@cli.command(name="socketio_client")
@click.option("-p", "--port")
@click.option("-n", "--name")
def client(name, port=10155):
    socketio_client(name, port)


def process_img(img):
    return process(img)
