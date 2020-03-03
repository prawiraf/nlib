import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # new

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # new
from flask_restful import Api, Resource # new
from middleware import middleware

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matadata.db'
app.wsgi_app = middleware(app.wsgi_app)
db = SQLAlchemy(app)
ma = Marshmallow(app) # new
api = Api(app) # new

@app.cli.command('initdb')
def initdb_command():
    """Initializes the database."""
    db.create_all()
    print('Initialized the database.')

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    name = db.Column(db.String(100))
    description = db.Column(db.String(255))
    type_data = db.Column(db.String(50))
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    def __repr__(self):
        return '<Metadata %s>' % self.filename

class MetadataSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "author", "description", "type_data", "date_added")

metadata_schema = MetadataSchema()
metadatas_schema = MetadataSchema(many=True)

class MetadataListResource(Resource):
    def get(self):
        metadatas = Metadata.query.all()
        return metadatas_schema.dump(metadatas)

class MetadataListResource(Resource):
    def get(self):
        metadatas = Metadata.query.all()
        return metadatas_schema.dump(metadatas)

    def post(self):
        try:
            new_data = Metadata(
                name=request.json['name'],
                author=request.json['author'],
                description=request.json['description'],
                type_data=request.json['type_data']
            )
        except:
            return jsonify({"message": "provide: name, author, description, and type_data"})
        db.session.add(new_data)
        db.session.commit()
        return metadata_schema.dump(new_data)

api.add_resource(MetadataListResource, '/metadata')

class MetadataResource(Resource):
    def get(self, metadata_id):
        metadata = Metadata.query.get_or_404(metadata_id)
        return metadata_schema.dump(metadata)

    def patch(self, metadata_id):
        metadata = Metadata.query.get_or_404(metadata_id)

        if 'name' in request.json:
            metadata.name = request.json['name']
        if 'description' in request.json:
            metadata.description = request.json['description']
        if 'author' in request.json:
            metadata.author = request.json['author']
        if 'type_data' in request.json:
            metadata.type_data = request.json['type_data']

        db.session.commit()
        return metadata_schema.dump(metadata)

    def delete(self, metadata_id):
        metadata = Metadata.query.get_or_404(metadata_id)
        db.session.delete(metadata)
        db.session.commit()
        return '', 204

api.add_resource(MetadataResource, '/metadata/<int:metadata_id>')

# Or specify port manually:
if __name__ == '__main__':
    port = int(os.environ.get('METADATA_SERVICE_PORT', 8082))
    app.run(host='0.0.0.0', port=port, debug=True)
