from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt

database = PyMongo()
bcrypt = Bcrypt()

def initialized_db(app):
  database.init_app(app, uri="mongodb://localhost:27017/user_db")
  db = database.db.client['user_db']
  return db


def init_bcrypt(app):
  bcrypt.init_app(app)