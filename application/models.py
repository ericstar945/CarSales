from enum import unique
import flask
from application import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30, unique=True)
    password = db.StringField()

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def get_password(self, password):
        return check_password_hash(self.password, password)

class Car(db.Document):

    car_id = db.IntField(max_length=10,unique=True)
    make = db.StringField(max_length=20)
    model = db.StringField(max_length=20)
    description = db.StringField(max_length=255)
    year = db.StringField(max_length=10)
    price = db.StringField(max_length=20)
    phone = db.StringField(max_length=10)
    picture = db.FileField()
    picture1 = db.FileField()
    picture2 = db.FileField()
    picname = db.StringField()
    picname1 = db.StringField()
    picname2 = db.StringField()
    

class Favorites(db.Document):
    user_id = db.IntField()
    car_id = db.IntField()