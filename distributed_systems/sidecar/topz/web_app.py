#!/usr/bin/python3
from flask import Flask

app = Flask(__name__)
port = 5001 


@app.route('/')
def welcome():
    return 'Salutations from a Flask web application running inside a docker container!', 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=port, debug=True)
