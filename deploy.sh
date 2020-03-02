source .env

export FLASK_APP=compress_service/app.py
flask run 
export FLASK_APP=metadata_service/app.py
flask run 