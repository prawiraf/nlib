import os
import uuid 
from flask import Flask, flash, request, redirect, url_for, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image, ExifTags


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
basedir = os.path.abspath(os.path.dirname(__file__))

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({"message": "put your file"})
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return jsonify({"message": "forbidden"})
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_name = f"{uuid.uuid1()}.{filename.split('.')[1]}"
            file.save(os.path.join(app.root_path, 'uploads/' + file_name))
            # getting and posting meta data
            img = Image.open(os.path.join(basedir, f'uploads/{file_name}'))
            img_exif = img.getexif()
            if img_exif:
                return jsonify({"url": f"/uploads/{file_name}", "metadata": img_exif})
            else:
                return jsonify({"url": f"/uploads/{file_name}"})

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
