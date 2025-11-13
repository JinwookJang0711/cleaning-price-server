import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 로컬 파일에서 직접 읽기
def load_prices():
    df = pd.read_excel("prices.xlsx")
    df = df.fillna(0)
    # price_server.py 너가 기존에 썼던 규칙 그대로 적용
    price_dict = dict(zip(df['옵션'], df['가격']))
    return price_dict

prices = load_prices()

@app.route("/price")
def get_price():
    option = request.args.get("option")
    if option not in prices:
        return jsonify({"error": "Invalid option"}), 400
    
    return jsonify({"price": prices[option]})

@app.route("/")
def home():
    return "Cleaning price API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
