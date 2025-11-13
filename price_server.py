import pandas as pd
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def load_prices():
    df = pd.read_excel("prices.xlsx")
    df = df.fillna(0)

    # 첫 번째 열: 지역
    regions = df.iloc[:, 0].tolist()

    # 나머지 열(평당단가, 원룸, 복층원룸...)
    cols = df.columns.tolist()[1:]

    data = {}

    for i, region in enumerate(regions):
        data[region] = {}
        for col in cols:
            data[region][col] = int(df.loc[i, col])

    return data

price_json = load_prices()

@app.route("/price")
def get_price():
    return jsonify(price_json)

@app.route("/")
def home():
    return "Cleaning price API running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
