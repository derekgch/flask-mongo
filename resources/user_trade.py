import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource
from flask_pymongo import ObjectId
from .user import User
from .trade import Trade


class UserTrade(Resource):    
  def get(self, user_info):
    found_user = User.find_user(self, user_info)
    if not found_user:
      return jsonify({'response':'user not foud'}, 404)
    found_trades = Trade.find_trade_by_user(self,str(found_user['_id']))
    
    found = []
    for trade in found_trades:
      trade['_id'] = str(trade["_id"])
      found.append(trade)
    
    return jsonify({'response':"trades found"}, found, 200)
    