
import os
import requests 
from flask import Flask, jsonify, request 
from flask_restful import Resource

SECRET_KEY = os.getenv("API_KEY")

class Stocks(Resource):
    def get(self, symbol):
        try:
            # https://cloud.iexapis.com/stable/tops?token=API_KEY&symbols=aapl
            base_url = f'https://cloud.iexapis.com/stable/tops?token={SECRET_KEY}&symbols={symbol}'
            response = requests.get(base_url)
            return response.json()
        except:
            return jsonify({"response":"Error"})