#!/bin/python3
import flask
import urllib.parse
import requests


app = flask.Flask(__name__)
domain_cache = {"localhost":{"ip":"127.0.0.1", "protocol":"http", "port":8080}}  # domain:port
domains = ["localhost"]


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def handle_request(path):
    domain = urllib.parse.urlparse(flask.request.base_url).hostname
    if domain in domains:
        response = requests.get("{}://{}:{}/{}".format(domain_cache[domain]['protocol'], domain_cache[domain]['ip'], domain_cache[domain]['port'], path), stream=True)
        resp = response
        return resp.raw.read(), resp.status_code, resp.headers.items()
    else:
        return flask.abort(404)



app.run()

