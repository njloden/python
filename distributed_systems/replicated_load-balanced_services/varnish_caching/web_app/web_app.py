#!/usr/bin/python3
from flask import Flask
import time
import string
import random

app = Flask(__name__)
port = 5001 
node = "node_01" 

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


@app.route('/long_query/<num>')
def long_running_query(num=1000000):
    """Sort an array of randomly generated numbers, and return the execution time. If no number
    is specified, then the default value of 1,000,000 will be used."""
    start_time = time.time()
    sorted_array = sorted([random.random() for i in range(int(num))])
    end_time = time.time()
    return 'It took {} seconds to sort an array of {} random numbers!'.format(str(end_time - start_time), num)


@app.route('/sleep')
def sleep_and_respond():
    """sleep for one second, and then send response to client"""
    time.sleep(1)
    return 'I was asleep for one whole second!'

def gen_instance_uuid():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range (20))


if __name__ == '__main__':
    uuid = gen_instance_uuid()
    app.run('0.0.0.0', port=port, debug=True)
