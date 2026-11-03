from datetime import datetime
import uuid

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

db = SQLAlchemy()


class Coordinator(db.Model):

    __tablename__ = "coordinators"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def set_password(self, password):

        self.password_hash = generate_password_hash(
            password
        )

    def check_password(self, password):

        return check_password_hash(
            self.password_hash,
            password
        )

    def __repr__(self):

        return f"<Coordinator {self.username}>"


class Report(db.Model):

    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    reference = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
        index=True
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    street = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    reporter_name = db.Column(
        db.String(100),
        nullable=False
    )

    reporter_cell = db.Column(
        db.String(15),
        nullable=False
    )

    photo_filename = db.Column(
        db.String(255)
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Open"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    
    @staticmethod
    def generate_reference():

        while True:

            reference = (
                "W42-" +
                uuid.uuid4().hex[:8].upper()
            )
            
            existing = Report.query.filter_by(
                reference=reference
            ).first()
            
            if not existing:
                
                return reference
            
    def __init__(
        self,
        category,
        street,
        description,
        reporter_name,
        reporter_cell,
        photo_filename=None
    ):

        self.reference = (
            Report.generate_reference()
        )

        self.category = category
        self.street = street
        self.description = description
        self.reporter_name = reporter_name
        self.reporter_cell = reporter_cell
        self.photo_filename = photo_filename

    def __repr__(self):

        return (
            f"<Report "
            f"{self.reference} "
            f"{self.category}"
            f"{self.status}>"
        )
        