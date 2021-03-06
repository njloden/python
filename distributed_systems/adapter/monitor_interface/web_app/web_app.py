#!/usr/bin/python3
from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import redis
import os

# define ports to be used for both flask web app and connection to redis container
app_port = 5001
redis_port = 6379

# define flask application
app = Flask(__name__)

# set env variable in order to expose the /metrics http endpoint
os.environ["DEBUG_METRICS"] = "false"

# initialize prometheus metrics collection
"""This will expose a /metrics endpoint for this web app which Prometheus will use to pull stats"""
metrics = PrometheusMetrics(app)

# initialize connection to redis cache using the name of the service specified in the docker-compose.yml file for the hostname 
cache = redis.Redis(host='redis', port=redis_port)


def page_hit_count():
    """will increment and return value of hits in redis key value store.
    The increment function will initialize a value of zero if it doesn't 
    already exist"""
    return cache.incr('hits')


@app.route('/')
def welcome():
    """get the current hit count from the redis cache, and return to requestor"""
    count = page_hit_count()
    return 'Hit Count: {}'.format(count), 200


if __name__ == '__main__':
    app.run('0.0.0.0', port=app_port, debug=True)
