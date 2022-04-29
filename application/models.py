import flask
from application import db

class User(db.Document):
    user_id = db.IntField(unique=True)
    first_name = db.StringField(max_length=50)
    last_name = db.StringField(max_length=50)
    email = db.StringField(max_length=30)
    password = db.StringField(max_length=30)

class Car(db.Document):

    car_id = db.StringField(max_length=10,unique=True)
    make = db.StringField(max_length=20)
    model = db.StringField(max_length=20)
    description = db.StringField(max_length=255)
    year = db.StringField(max_length=10)
    price = db.StringField(max_length=20)
    picture = db.FileField()

class Favorites(db.Document):
    user_id = db.IntField()
    car_id = db.StringField(max_length=10)