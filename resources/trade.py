
import requests 
import datetime

from flask import Flask, jsonify, request 
from flask_restful import Resource
from flask_pymongo import ObjectId

from database.db import database
from .user import User
from .stock import Stock



class Trade(Resource):
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
        trade_data["timestamp"] = datetime.datetime.now()
        if not self.validate_trade(data):
            return jsonify({"response":"trade info not valid"},trade_data, 400)
        current_price = self.get_current_stock_price(trade_data.get('symbol'))
        if not current_price:
          return jsonify({"response":"trade symbol not valid"},trade_data, 400)
        trade_data["price"] = current_price
        trade_data['price_timestamp'] = datetime.datetime.now()
        inserted = database.db.trades.insert_one(trade_data)
        traded_result = database.db.trades.find_one({'_id':inserted.inserted_id})
        traded_result['_id'] = str(traded_result['_id'])
        return jsonify({"response":"Successeful", 'trade result': traded_result}, 200)

    def find_trade(self, trade_id):
        return database.db.trades.find_one({"_id":ObjectId(trade_id)})
      
    def find_trade_by_user(self,user_id):
        return database.db.trades.find({'user_id':user_id})
    
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
    
    def get_current_stock_price(self, symbol):
      quote = Stock.get_price(self, symbol).json()
      
      if not quote:
        return None
      print("========", quote[0])
      return quote[0]['lastSalePrice']
    
    def validate_trade(self, data):
        return data.get('symbol') and data.get('price') and data.get('quantity') and data.get('timestamp') and data.get('action')
        
        
        