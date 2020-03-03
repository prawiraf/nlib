import os

from flask import Flask, request, jsonify, render_template
from middleware import middleware

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route('/upload', methods=["GET", "POST"])
def home():
    app.wsgi_app = middleware(app.wsgi_app)
    return render_template("upload.html")

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('COMPRESS_SERVICE_PORT', 8081))
    app.run(host='0.0.0.0', port=port)
