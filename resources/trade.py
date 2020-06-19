
import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource
from flask_pymongo import ObjectId
from database.db import database
from .user import User



class Trades(Resource):
    def get(self, trade_id):
        found = self.find_trade(trade_id)
        if not found:
            return jsonify({"response":"Not Found"} , 400)
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
        
        trade_data = self.trade_data(data, found_user)
        if not self.validate_trade(data):
            return jsonify({"response":"trade info not valid"},trade_data, 400)
        
        inserted = database.db.trades.insert_one(trade_data)
        
        return jsonify({"response":"Successeful", 'trade ID': str(inserted.inserted_id)}, 200)

    def find_trade(self, trade_id):
        return database.db.trades.find_one({"_id":ObjectId(trade_id)})
    
    def validate_user(self, data):
        username = data.get('username')
        user_id = data.get('user_id')
        if not user_id:
            found = User.find_user(self, username)
        else:
            found = User.find_user(self, user_id)
        return found
      
    def trade_data(self, data , found_user):
      return  {
            "user_id":found_user["_id"],
            "symbol":data.get('symbol'),
            "price":data.get('price'),
            "quantity":data.get('quantity'),
            "action":data.get('action'),
            "timestamp":data.get('timestamp')
        }
    
    def validate_trade(self, data):
        return data.get('symbol') and data.get('price') and data.get('quantity') and data.get('timestamp') and data.get('action')
        
        
        