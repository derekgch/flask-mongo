

import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource
from flask_pymongo import ObjectId
from database.db import database, bcrypt

class User(Resource):    
    def get(self, user_info):
        found = self.find_user(user_info)
        
        return jsonify({"response":found})
    
    def post(self):
      try:
        
        data = request.get_json()
        
        if not data:
            return jsonify({"response":"ERROR. Empty payload"})
        else:
            username = data.get('username')
            if database.db.users.find_one({'username':username}):
                return jsonify({"response":"ERROR. Already exisits"})
            else:
                data_hashed = self.hash_password(data)
                database.db.users.insert_one(data_hashed)
                found = self.find_user(username)
                
                return jsonify({"response":self.trip_pw_hash(found)})
      except Exception as e:
        return jsonify({"response:":str(e)}, 400)
                
    
    def delete(self, user_info):
        found = self.find_user(user_info)
        if not found:
            return jsonify({'response':"user not found", 'user':user_info})
        database.db.users.delete_one({'_id':ObjectId(found['_id'])})
        
        return jsonify({'response':'user deteled', 'user': user_info})
    
    def patch(self, user_id):
        return jsonify({'patch user':'derek', 'user_id':user_id})
    
    def find_user(self, user_info):
        found = False
        if(ObjectId.is_valid(user_info)):
            found = database.db.users.find_one({"_id":ObjectId(user_info)})
            
        if not found:
            found = database.db.users.find_one({"username":user_info})
        
        if found:
            found['_id'] = str(found['_id'])
            found['password'] = "****"
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
        