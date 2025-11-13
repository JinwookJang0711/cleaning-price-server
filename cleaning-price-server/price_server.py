from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)  # HTML 접근 허용

@app.route("/price")
def get_price():
    path = "prices.xlsx"
    df = pd.read_excel(path)
    data = {}

    for _, row in df.iterrows():
        region = str(row["지역"]).strip()
        data[region] = {
            "평당단가": int(row["평당단가"]),
            "원룸": int(row["원룸"]),
            "복층원룸": int(row["복층원룸"]),
            "1.5룸": int(row["1.5룸"]),
            "투룸": int(row["투룸"]),
            "쓰리룸": int(row["쓰리룸"])
        }

    return jsonify(data)

if __name__ == "__main__":
    print("✅ 가격 서버 실행 중... (http://localhost:5001/price)")
    app.run(host="0.0.0.0", port=5001)
