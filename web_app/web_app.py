#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
port = REPLACE_WITH_PORT 
node = REPLACE_WITH_INSTANCE_NUMBER 

@app.route('/')
def welcome():
    return 'Hello from web app instance {}!'.format(node), 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=port, debug=True)
