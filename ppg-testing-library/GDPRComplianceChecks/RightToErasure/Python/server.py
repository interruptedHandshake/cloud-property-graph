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
    if user_db_collection.find( { "username": data['username'] } ).count() > 0:
        return "Conflict", 409
    else:
        user_db_collection.delete_one({"username": data['username']})
        # inform external advertising server about the deletion
        requests.delete("ext-ad-server.com/data", json = data)
        return "Created", 201

@app.route("/store_data", methods=['POST'])
def parse_data():
    req = request.json
    data = {
        "username": req['username'],
        "notes": req['notes']
    }
    if user_db_collection.find( { "username": data['username'] } ).count() > 0:
        return "Conflict", 409
    else:
        # save data to database
        user_db_collection.insert_one(data)
        # send data to external advertising server
        url = 'ext-ad-server.com/data'
        requests.put(url, json = data)
        return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)