#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
port = 5003
node = 'Node 3'

@app.route('/')
def welcome():
    return 'Hello from {}!'.format(node), 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=port, debug=True)
