from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    # define the database schema of table 'Note'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # foreign key relationship
    # foreign key is a column in your database that references another column in another database

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #--> this one to many relationship, where one user have many notes (parent --> many children)
    # class User, data 'id' --> it needs lowercas user in this one (child)

class User(db.Model, UserMixin):
    # define the database schema of table 'User'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(255))
    notes = db.relationship('Note') # but you do need capital for this for the parent
