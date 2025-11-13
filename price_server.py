from flask import Flask, jsonify
import pandas as pd
import requests
from io import BytesIO
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔥 너의 OneDrive "다운로드 링크" 로 변경해야 함
EXCEL_URL = "https://onedrive.live.com/download?cid=XXXXX&resid=YYYY"

def load_prices():
    try:
        # OneDrive에서 파일 다운로드
        response = requests.get(EXCEL_URL)
        response.raise_for_status()  # 다운로드 오류 체크

        excel_bytes = BytesIO(response.content)

        df = pd.read_excel(excel_bytes)  # 엑셀 읽기
        return df.to_dict(orient="records")

    except Exception as e:
        print("엑셀 읽기 오류:", e)
        return {"error": str(e)}

@app.route("/")
def home():
    return "입주청소 가격 서버 작동 중"

@app.route("/price")
def get_price():
    return jsonify(load_prices())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
