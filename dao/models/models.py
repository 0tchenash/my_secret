from files.setup_db import db
from marshmallow import Schema, fields
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    password = fields.Str()

class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")
    username = db.Column(db.String)
    text = db.Column(db.String)

class ContactSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    username = fields.Str()
    text = fields.Str()
