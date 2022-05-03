from multiprocessing import connection
from flask import Flask
import pymongo
from config import Config
from flask_mongoengine import MongoEngine
from flask_pymongo import MongoClient 
import gridfs

app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)
connection = MongoClient('localhost', 27017)
database = connection['CarDB']
fs = gridfs.GridFS(database)

from application import routes

