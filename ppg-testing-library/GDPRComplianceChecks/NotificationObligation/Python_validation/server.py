#!/usr/bin/env python3

from flask import Flask, request
from pymongo import MongoClient, database
import requests

mongo_host = "mongo"
user_db_client = MongoClient("mongodb://mongo:27017/")
user_db = user_db_client.userdata
user_db_collection = user_db.records

app = Flask(__name__)

@app.route("/data", methods=['DELETE'])
def parse_data():
    req = request.json
    data = {
        "username": req['username'],
        "notes": req['notes']
    }

    user_db_collection.delete_one({"username": data['username']})
    # VALIDATION: no external advertising server is informed about the deletion
    return "OK", 200

@app.route("/data", methods=['PUT'])
def parse_data():
    req = request.json
    data = {
        "username": req['username'],
        "notes": req['notes']
    }
    user_db_collection.update_one({"username": data['username']}, {"$set": {"notes": data['notes']}})
    # VALIDATION: no external advertising server is informed about the rectification
    return "OK", 200

@app.route("/data", methods=['POST'])
def parse_data():
    req = request.json
    data = {
        "username": req['username'],
        "notes": req['notes']
    }
    url = "ext-ad-server.com/data"
    # send notes to external advertising server
    requests.post(url, json = data['notes'])
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)