from flask import Flask, request
import os
import csv_queue
import json

app = Flask(__name__)

@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/upload", methods=['POST'])
def upload():
    return json.dumps({'success':True})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
