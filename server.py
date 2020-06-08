# using flask_restful 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from flask_pymongo import PyMongo, ObjectId
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os
import requests 

load_dotenv()

SECRET_KEY = os.getenv("API_KEY")

# creating the flask app 
app = Flask(__name__) 
app.config['MONGO_DBNAME'] = 'user_db'
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"
mongo = PyMongo(app)
# creating an API object 
api = Api(app) 
bcrypt = Bcrypt(app)

client = mongo.db.client
db = client['user_db']
# making a class for a particular resource 
# the get, post methods correspond to get and post requests 
# they are automatically mapped by flask_restful. 
# other methods include put, delete, etc. 
class Hello(Resource): 
  
    # corresponds to the GET request. 
    # this function is called whenever there 
    # is a GET request for this resource 
    def get(self): 
  
        return jsonify({'message': 'hello world'}) 
  
    # Corresponds to POST request 
    def post(self): 
          
        data = request.get_json()     # status code 
        return jsonify({'data': data}), 201
  
  
# another resource to calculate the square of a number 
class All_user_id(Resource): 
  
    def get(self): 
  
        return jsonify() 

class User(Resource):
    
    def get(self, user_info):
        found = self.find_user(user_info)
        
        return jsonify({"response":found})
    
    def post(self, user_info):
        data = request.get_json()
        
        if not data:
            return jsonify({"response":"ERROR. Empty payload"})
        else:
            username = data.get('username')
            if db.users.find_one({'username':username}):
                return jsonify({"response":"ERROR. Already exisits"})
            else:
                data_hashed = self.hash_password(data)
                db.users.insert_one(data_hashed)
                found = self.find_user(username)
                
                return jsonify({"response":self.trip_pw_hash(found)})
                
    
    def delete(self, user_info):
        found = self.find_user(user_info)
        if not found:
            return jsonify({'response':"user not found", 'user':user_info})
        result = db.users.delete_one({'_id':ObjectId(found['_id'])})
        
        print('result======', {'_id':found['_id']})
        print('result======', result.acknowledged, result.deleted_count)
        return jsonify({'response':'user deteled', 'user': user_info})
    
    def patch(self, user_id):
        return jsonify({'patch user':'derek', 'user_id':user_id})
    
    def find_user(self, user_info):
        found = db.users.find_one({"_id":user_info})
        if not found:
            found = db.users.find_one({"username":user_info})
        
        if found:
            print('message:=====', found)
            found['_id'] = str(found['_id'])
        return found
    
    def hash_password(self, data):
        password = data.get('password')
        if not password:
            password = '123456789'
        pw_hash = bcrypt.generate_password_hash(password)
        data['password'] = pw_hash
        return data
    
    def trip_pw_hash(self, data):
        data['password'] = '****'
        return data
        
class Stocks(Resource):
    def get(self, symbol):
        try:
            # https://cloud.iexapis.com/stable/tops?token=API_KEY&symbols=aapl
            base_url = f'https://cloud.iexapis.com/stable/tops?token={SECRET_KEY}&symbols={symbol}'
            response = requests.get(base_url)
            print("=====", base_url,response.status_code)
            return response.json()
        except:
            return jsonify({"response":"Error"})
        
            
    
    
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Stocks, '/api/stock/<string:symbol>') 
api.add_resource(All_user_id, '/api/all') 
api.add_resource(User, '/api/user/<string:user_info>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 