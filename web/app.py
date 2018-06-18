from flask import Flask, request
from werkzeug.utils import secure_filename
import os

import csv_queue

app = Flask(__name__)

@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/upload", methods=['POST'])
def upload():
    file = request.files["file"]
    r = csv_queue.CsvReader(secure_filename(file.filename),
        os.getenv("QUEUE_NAME"),
        os.getenv("QUEUE_IP")
    )
    r.send()


    return "file read ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
