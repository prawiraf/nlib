source .env

# FRONT_SERVICE_PORT=20586
# COMPRESS_SERVICE_PORT=20587
# UPLOAD_SERVICE_PORT=20588
# METADATA_SERVICE_PORT=20589
# INTERNAL_HOST=http://0.0.0.0
kill -9 $(lsof -t -i:20587)
kill -9 $(lsof -t -i:20588)
kill -9 $(lsof -t -i:20589)

FLASK_RUN_PORT=20587 FLASK_APP=compress_service/app.py FLASK_RUN_HOST=0.0.0.0 FLASK_ENV=development flask run &
FLASK_RUN_PORT=20588 FLASK_APP=upload_service/app.py FLASK_RUN_HOST=0.0.0.0 FLASK_ENV=development flask run &
FLASK_RUN_PORT=20589 FLASK_APP=metadata_service/app.py FLASK_RUN_HOST=0.0.0.0 FLASK_ENV=development flask run &