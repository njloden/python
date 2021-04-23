#!/usr/bin/python3
import flask
import time

app = flask.Flask(__name__)
port = 5002 
node = "node_02" 

@app.route('/')
@app.route('/test/<num>')
def welcome(num=1):
    """provide generic response to requests to root and /test/<num> endpoints"""
    response = flask.Response('Hello from web app instance {}!'.format(node))
    response.headers['X-Backend-Node'] = node 
    return response


@app.route('/time')
def time_stamp():
    current_time = 'Date/Time: {}'.format(time.strftime('%m/%d/%Y %H:%M:%S'))
    response = flask.Response(current_time)
    response.headers['X-Backend-Node'] = node
    return response


@app.route('/sleep')
def sleep_and_respond():
    """sleep for one second, and then send response to client"""
    time.sleep(3)
    response = flask.Response('I was asleep for one whole second!')
    response.headers['X-Backend-Node'] = node
    return response


if __name__ == '__main__':
    app.run('0.0.0.0', port=port, debug=True)
