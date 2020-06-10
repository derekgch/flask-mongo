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
        db.users.delete_one({'_id':ObjectId(found['_id'])})
        
        return jsonify({'response':'user deteled', 'user': user_info})
    
    def patch(self, user_id):
        return jsonify({'patch user':'derek', 'user_id':user_id})
    
    def find_user(self, user_info):
        found = False
        if(ObjectId.is_valid(user_info)):
            found = db.users.find_one({"_id":ObjectId(user_info)})
            
        if not found:
            found = db.users.find_one({"username":user_info})
        
        if found:
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
            return response.json()
        except:
            return jsonify({"response":"Error"})
        
class Trades(Resource):
    def get(self, trade_id):
        found = self.find_trade(trade_id)
        if not found:
            return jsonify({"response":"Not Found", "status":404})
        found["_id"] = str(found["_id"])
        return jsonify({"response":found})
    
    def post(self):
        data = request.get_json()
        if not data:
            return jsonify({"response":"ERROR. Empty payload"})
        else:
            found_user = self.validate_user(data)

            if not found_user:
                return jsonify({"response":"not found"}, 404)
        
        trade_data = {
            "user_id":found_user["_id"],
            "symbol":data.get('symbol'),
            "price":data.get('price'),
            "quantity":data.get('quantity'),
            "timestamp":data.get('timestamp')
        }
        
        if not self.validate_trade(data):
            return jsonify({"response":"trade info not valid"},trade_data, 400)
        
        inserted = db.trades.insert_one(trade_data)
        
        return jsonify({"response":"Successeful", 'trade ID': str(inserted.inserted_id)}, 200)

    def find_trade(self, trade_id):
        return db.trades.find_one({"_id":ObjectId(trade_id)})
    
    def validate_user(self, data):
        username = data.get('username')
        user_id = data.get('user_id')
        if not user_id:
            found = User.find_user(self, username)
        else:
            found = User.find_user(self, user_id)
        return found
    
    def validate_trade(self, data):
        return data.get('symbol') and data.get('price') and data.get('quantity') and data.get('timestamp')
        
        
        
        
            
    
    
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Stocks, '/api/stock/symbol/<string:symbol>')
api.add_resource(Trades, '/api/trade/<string:trade_id>', '/api/trade')
api.add_resource(All_user_id, '/api/all') 
api.add_resource(User, '/api/user/<string:user_info>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 