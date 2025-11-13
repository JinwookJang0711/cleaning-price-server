import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 엑셀 불러오기
def load_prices():
    df = pd.read_excel("prices.xlsx")
    df = df.fillna(0)

    # 지역명 → 가격표(dict) 형태로 변환
    price_dict = {}

    for _, row in df.iterrows():
        region = row["지역"]

        # 지역별 가격표
        price_dict[region] = {
            "평당단가": int(row["평당단가"]),
            "원룸": int(row["원룸"]),
            "복층원룸": int(row["복층원룸"]),
            "1.5룸": int(row["1.5룸"]),
            "투룸": int(row["투룸"]),
            "쓰리룸": int(row["쓰리룸"])
        }

    return price_dict


prices = load_prices()


@app.route("/price")
def get_price():
    region = request.args.get("region")
    room = request.args.get("room")   # ex: 원룸 / 투룸 / 평당단가

    if region not in prices:
        return jsonify({"error": "Invalid region"}), 400

    if room not in prices[region]:
        return jsonify({"error": "Invalid room type"}), 400

    return jsonify({
        "region": region,
        "room": room,
        "price": prices[region][room]
    })


@app.route("/")
def home():
    return "Cleaning price API is running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
