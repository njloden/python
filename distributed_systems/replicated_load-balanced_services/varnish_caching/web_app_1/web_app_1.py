#!/usr/bin/python3
import flask
import time

app = flask.Flask(__name__)
port = 5001 
node = "node_01" 

@app.route('/')
def welcome():
    response = flask.Response('Hello from web app instance {}!'.format(node))
    response.headers['X-Backend-Node'] = node 
    return response


@app.route('/time')
def time_stamp():
    current_time = '{}'.format(time.strftime('%m/%d/%Y %H:%M:%S'))
    response = flask.Response(''.format(current_time))
    response.headers['X-Backend-Node'] = node
    return response


@app.route('/sleep')
def sleep_and_respond():
    """sleep for one second, and then send response to client"""
    time.sleep(1)
    response = flask.Response('I was asleep for one whole second!')
    response.headers['X-Backend-Node'] = node
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', port=port, debug=True)
