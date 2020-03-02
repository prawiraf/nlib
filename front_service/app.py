from flask import Flask, request, jsonify
from .models import MetaData

import zlib
import os

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if(request.method == "POST"):
        try:
            file_ = request.files['file'].read()
            compressed = zlib.compress(file_)
            return compressed
        except:
            return jsonify({"message": "plese input the file to be compressed"})
    else:
        return jsonify({"sanity": "checked"})

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('COMPRESS_SERVICE_PORT', 8081))
    app.run(host='0.0.0.0', port=port)
