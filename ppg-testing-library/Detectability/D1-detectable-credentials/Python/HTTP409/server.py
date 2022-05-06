#!/usr/bin/env python3

from flask import Flask, request

app = Flask(__name__)

# Detectability threat results from leaking information about existing accounts
@app.route("/account", methods=['POST'])
def collect_data():
    content = request.json
    return "Conflict", 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)