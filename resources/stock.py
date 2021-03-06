
import os
import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource

SECRET_KEY = os.getenv("API_KEY")

class Stock(Resource):
    def get(self, symbol):
        try:
            response = self.get_price(symbol)
            return response.json()
        except:
            return jsonify({"response":"Error"}, 404)
          
    def get_price(self, symbol):
            # https://cloud.iexapis.com/stable/tops?token=API_KEY&symbols=aapl
      base_url = f'https://cloud.iexapis.com/stable/tops?token={SECRET_KEY}&symbols={symbol}'
      return requests.get(base_url)