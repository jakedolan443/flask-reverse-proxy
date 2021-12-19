from flask import Flask,request,redirect,Response
import requests


app = Flask(__name__)


config = {"domain.com":"https://127.0.0.1:5623"}   # domain.com is hosted internally at 127.0.0.1:5623



@app.route("/<path:path>", methods=["GET", "POST", "DELETE"])
def route(path):
    req_host = request.headers['Host']
    try:
        location = config[req_host]
    except KeyError:
        return "Not found", 404
    return request_to(location, path, method=request.method)

def request_to(location, path, method="GET"):
    if request.method=="GET":
        resp = requests.get("{}/{}".format(location, path))
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in  resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=="POST":
        resp = requests.post("{}/{}".format(location, path),json=request.get_json())
        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        response = Response(resp.content, resp.status_code, headers)
        return response
    elif request.method=="DELETE":
        resp = requests.delete("{}/{}".format(location, path)).content
        response = Response(resp.content, resp.status_code, headers)
        return response
    
