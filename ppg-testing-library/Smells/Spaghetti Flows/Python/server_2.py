#!/usr/bin/env python3

from flask import Flask, request
import json
import requests
import logging
import os, sys

app = Flask(__name__)

# Smell results from several microservices processing the data
@app.route("/data2", methods=['POST'])
def collect_data():
    content = request.json
    return "OK", 200

if __name__ == '__main__':
    logging.info("start at port 8080")
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)