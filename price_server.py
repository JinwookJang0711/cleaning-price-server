from flask import Flask, jsonify
import pandas as pd
import requests
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔥 변환된 OneDrive 다운로드 링크 (100% 작동)
EXCEL_URL = "https://onedrive.live.com/download?resid=9A7ECB699D7A2B22!ETRb9Rs2kKhEo3ummWLSPhwBXkPBDDuxPADaGrgBJFq3Dg"

def load_prices():
    try:
        response = requests.get(EXCEL_URL)
        response.raise_for_status()
        df = pd.read_excel(BytesIO(response.content))
        return df.to_dict(orient="records")
    except Exception as e:
        return {"error": str(e)}

@app.route("/")
def home():
    return "입주청소 가격 서버 작동 중"

@app.route("/price")
def get_price():
    return jsonify(load_prices())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
