import os
import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource, Api 
from dotenv import load_dotenv
from database.db import initialized_db, init_bcrypt,database
from flask_bcrypt import Bcrypt
from resources.user import User
from resources.stock import Stock
from resources.trade import Trade
from resources.user_trade import UserTrade

load_dotenv()

# creating the flask app 
app = Flask(__name__) 
app.config['MONGO_DBNAME'] = 'user_db'
app.config["MONGO_URI"] = "mongodb://localhost:27017/user_db"

api = Api(app) 
initialized_db(app)
init_bcrypt(app)


api.add_resource(User, '/api/user/', '/api/user/<string:user_info>' ) 
api.add_resource(Stock, '/api/stock/symbol/<string:symbol>')
api.add_resource(Trade, '/api/trade/', '/api/trade/<string:trade_id>')
api.add_resource(UserTrade, '/api/user/trades/<string:user_info>') 


# driver function 
if __name__ == '__main__': 
    app.run(debug = True) 