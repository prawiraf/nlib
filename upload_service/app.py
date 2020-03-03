import os
import uuid 
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags
from middleware import middleware


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}


app = Flask(__name__)
app.wsgi_app = middleware(app.wsgi_app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))

def create_metadata(file, file_name):
    url = f"{os.environ['INTERNAL_HOST']}:{os.environ['METADATA_SERVICE_PORT']}/metadata"
    auth_token = request.headers.environ['HTTP_AUTHORIZATION']
    cdn = f"{os.environ['INTERNAL_HOST']}:{os.environ['UPLOAD_SERVICE_PORT']}"

    data = {
        "name": file_name,
        "author": "uploader",
        "description": 
            f"metadata of object uploaded at out service: link at: {cdn}",
        "type_data": "uploaded file information"
    }
    r = requests.post(url, 
            headers={'Authorization': auth_token})
    return r

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"message": "put your file"})
        file = request.files['file']
        if file.filename == '':
            return jsonify({"message": "forbidden"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name = f"{uuid.uuid1()}.{filename.split('.')[1]}"
            file.save(os.path.join(basedir, 'uploads/' + file_name))
            try:
                r = create_metadata(file, filename)
                return jsonify(r)
            # getting and posting meta data
            except Exception as e:
                print(e)
                return jsonify({"url": f"{request.host_url}uploads/{file_name}"})
    return jsonify({"sanity": "checked"})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('UPLOAD_SERVICE_PORT', 8083))
    app.run(host='0.0.0.0', port=port)
