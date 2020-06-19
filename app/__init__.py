
# from flask import Flask, jsonify, request 
# from flask_restful import Resource, Api 
# from flask_pymongo import PyMongo, ObjectId
# from flask_bcrypt import Bcrypt
# from dotenv import load_dotenv

# from instance.config import app_config
    
# def create_app(config_name):
#   app = Flask(__name__, instance_relative_config=True)
#   app.config.from_object(app_config[config_name])
#   app.config.from_pyfile('config.py')
  
#   app.config['MONGO_DBNAME'] = 'user_db'
#   app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"
  
#   mongo = PyMongo(app)
#   client = mongo.db.client
#   db = client['user_db']
  
#   api = Api(app) 
#   bcrypt = Bcrypt(app)
  
#   return app