# using flask_restful 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from flask_pymongo import PyMongo, ObjectId
  
# creating the flask app 
app = Flask(__name__) 
app.config['MONGO_DBNAME'] = 'user_db'
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"
mongo = PyMongo(app)
# creating an API object 
api = Api(app) 

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
                db.users.insert_one(data)
                found = self.find_user(username)
                return jsonify({"response":found})
                
    
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
        
  
# adding the defined resources along with their corresponding urls 
api.add_resource(Hello, '/') 
api.add_resource(All_user_id, '/api/all') 
api.add_resource(User, '/api/user/<string:user_info>') 
  
  
# driver function 
if __name__ == '__main__': 
  
    app.run(debug = True) 