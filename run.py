import os
import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from dotenv import load_dotenv
from database.db import initialized_db, init_bcrypt,database
from flask_bcrypt import Bcrypt
from resources.user import User

load_dotenv()

# creating the flask app 
app = Flask(__name__) 
app.config['MONGO_DBNAME'] = 'user_db'
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"

api = Api(app) 
initialized_db(app)
init_bcrypt(app)

db = database.db

class Hello(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
        found = db.users.find_one({'username':'test60'})
        print(found)
        found['_id'] = '***'
        found['password'] = "****"
        return jsonify({'message': 'hello world'}, found) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        return jsonify({'data': data}), 201

api.add_resource(Hello, '/') 
api.add_resource(User, '/api/user/<string:user_info>') 

# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 