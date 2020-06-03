# using flask_restful 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from flask_pymongo import PyMongo
  
# creating the flask app 
app = Flask(__name__) 
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"
mongo = PyMongo(app)
# creating an API object 
api = Api(app) 
  
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
class Square(Resource): 
  
    def get(self, num): 
  
        return jsonify({'square': num**2}) 

class User(Resource):
    
    def get(self, user_id):
        return jsonify({'user':'derek', 'user_id':"001"})
    
    def post(self, user_id):
        print('message:=====', user_id)
        return jsonify({'user':'derek', 'user_id':user_id})
    
    def delete(self, user_id):
        return jsonify({'delete user':'derek', 'user_id':user_id})
    
    def patch(self, user_id):
        return jsonify({'patch user':'derek', 'user_id':user_id})
        
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(Square, '/square/<int:num>') 
api.add_resource(User, '/api/user/<string:user_id>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 