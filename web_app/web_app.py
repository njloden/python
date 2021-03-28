#!/usr/bin/python3
from flask import Flask
import time
import string
import random

app = Flask(__name__)
port = REPLACE_WITH_PORT 
node = REPLACE_WITH_INSTANCE_NUMBER 

@app.route('/')
def welcome():
    return 'Hello from web app instance {}!'.format(node), 200


@app.route('/ping')
def ping():
    """created a basic flask server with the route /ping.
    The server will return a response with “PONG” for GET requests
    to /ping route."""
    return 'PONG', 200


@app.route('/time')
def time_stamp():
    current_time = '{}'.format(time.strftime('%m/%d/%Y %H:%M:%S'))
    return current_time, 200


@app.route('/uuid')
def instance_uuid():
    return 'Instance UUID: {}'.format(uuid)


def gen_instance_uuid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range (20))


if __name__ == '__main__':
    uuid = gen_instance_uuid()
    app.run('0.0.0.0', port=port, debug=True)
