from flask import Flask, request, jsonify, send_from_directory

import zlib
import os
import uuid 
import zipfile
import gzip

app = Flask(__name__)

COMPRESSED_FOLDER = 'compressed'
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/', methods=["GET", "POST"])
def home():
    if(request.method == "POST"):
        try:
            file_ = request.files['file'].read()
            filename = f"{uuid.uuid1()}.zip"
            with gzip.open('./compressed/' + filename, 'wb') as f:
                f.write(file_)
            return jsonify({"url": f"/compressed/{filename}"})
        except Exception as e:
            print(e)
            return jsonify({"message": "plese input the file to be compressed"})
    else:
        return jsonify({"sanity": "checked"})

@app.route('/compressed/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['COMPRESSED_FOLDER'],
                               filename)

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('COMPRESS_SERVICE_PORT', 8081))
    app.run(host='0.0.0.0', port=port)
