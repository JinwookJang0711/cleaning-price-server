import pandas as pd
import requests
from flask import Flask, jsonify
from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)

# 🔥 OneDrive 다운로드 링크 (너의 링크 그대로 넣음)
EXCEL_URL = "https://1drv.ms/x/c/9a7ecb699d7a2b22/ETRb9Rs2kKhEo3ummWLSPhwBXkPBDDuxPADaGrgBJFq3Dg?e=kRO7hW&download=1"

def load_prices():
    """OneDrive에서 엑셀을 다운로드해서 pandas로 읽어오기"""
    try:
        file_data = requests.get(EXCEL_URL)
        file_data.raise_for_status()

        df = pd.read_excel(BytesIO(file_data.content))
        df = df.fillna(0)

        price_dict = {}

        for _, row in df.iterrows():
            region = row["지역"]
            price_dict[region] = {
                "평당단가": int(row["평당단가"]),
                "원룸": int(row["원룸"]),
                "복층원룸": int(row["복층원룸"]),
                "1.5룸": int(row["1.5룸"]),
                "투룸": int(row["투룸"]),
                "쓰리룸": int(row["쓰리룸"]),
            }

        return price_dict

    except Exception as e:
        return {"error": str(e)}

@app.route("/price")
def get_price():
    """호출할 때마다 최신 엑셀값으로 JSON 생성"""
    prices = load_prices()

    if "error" in prices:
        return jsonify({"error": prices["error"]}), 500

    return jsonify(prices)

@app.route("/")
def home():
    return "Cleaning price API is running"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
