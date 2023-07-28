from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash

class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(64), nullable=True)
    hobby = db.Column(db.String(64))
    desc = db.Column(db.String(256))
    added_by = db.relationship('User', backref = "profile")

    def __init__(self, name, age, gender, hobby, desc):
        self.name = name
        self.age = age
        self.gender = gender
        self.hobby = hobby
        self.desc = desc

    def to_json(self):
        return {
            "name":self.name,
            "age" :self.age,
            "gender" :self.gender,
            "hobby" : self.hobby,
            "desc" : self.desc
        }

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    db_user_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    email = db.Column(db.String(120), unique=True, nullable=True)
    password = db.Column(db.String(64), unique=True, nullable=True)

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf-8')
    
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_json(self):
        return {
            "email":self.email,
            "password":self.password
        }