from flask import Flask, request
from werkzeug.utils import secure_filename
import os
import io

import csv_queue

app = Flask(__name__)

@app.route("/")
def root():
    return app.send_static_file("index.html")


@app.route("/upload", methods=['POST'])
def upload():
    if "file" in request.files:
        file = request.files["file"]
        file_data = io.StringIO(file.stream.read().decode("utf-8"))

        r = csv_queue.CsvReader(file_data,
            os.getenv("QUEUE_NAME"),
            os.getenv("QUEUE_IP")
        )
        r.send()

        return "file read ok"
    else:
        return "file read not ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
