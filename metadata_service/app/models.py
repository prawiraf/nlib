from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class Metadata(db.Model):
    id = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True)
    filename = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(80), unique=True, nullable=True)
    date_added = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '<Metadata {}>'.format(self.filename)  