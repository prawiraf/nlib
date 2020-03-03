from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy # new

from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # new
from flask_restful import Api, Resource # new

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///matadata.db'
db = SQLAlchemy(app)
ma = Marshmallow(app) # new
api = Api(app) # new

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(50))
    description = db.Column(db.String(255))

    def __repr__(self):
        return '<Metadata %s>' % self.filename

class MetadataSchema(ma.Schema):
    class Meta:
        fields = ("id", "filename", "description")

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
        new_post = Metadata(
            filename=request.json['filename'],
            description=request.json['description']
        )
        db.session.add(new_post)
        db.session.commit()
        return metadata_schema.dump(new_post)

api.add_resource(MetadataListResource, '/metadata')

class MetadataResource(Resource):
    def get(self, metadata_id):
        metadata = Metadata.query.get_or_404(metadata_id)
        return metadata_schema.dump(metadata)

    def patch(self, metadata_id):
        metadata = Metadata.query.get_or_404(metadata_id)

        if 'filename' in request.json:
            metadata.title = request.json['filename']
        if 'description' in request.json:
            metadata.content = request.json['description']

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
