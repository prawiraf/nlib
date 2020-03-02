from flask import Flask, request, jsonify
from PIL import Image, ExifTags
from PIL import Image

import zlib
import os
import sqlite3

@app.route('/', methods=["GET", "POST"])
def home():
    if(request.method == "POST"):
        if(request.is_json):
            data = request.json

            return data['filename']
        else:
            return jsonify({"message": "content accepted: json"})
    else:
        return jsonify({"sanity": "checked"})

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('METADATA_SERVICE_PORT', 8082))
    app.run(host='0.0.0.0', port=port)
