from flask import Flask, request
import requests
import json

app = Flask(__name__)

# 🔐 توكن البوت
TELEGRAM_TOKEN = '8111821598:AAF0xwexeGrgRn8OmPzbFdM5ZJb3uiO5Cqg'

# 👥 قائمة الـ Chat IDs
CHAT_IDS = [
    '-1002702794040',
    '8124167090',
    '456789123'
]

@app.route('/', methods=['GET'])
def home():
    return "✅ Flask server is running and ready to receive TradingView alerts."

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # محاولة قراءة JSON من TradingView
        data = request.get_json(force=True, silent=True)
        print("📩 Raw request data:", request.data.decode("utf-8"))
        print("📦 Parsed JSON:", data)

        # استخراج الرسالة المناسبة
        if data:
            # لو TradingView أرسل JSON كامل
            message = json.dumps(data, indent=2)
        else:
            # لو أرسل نص عادي
            message = request.data.decode("utf-8")

        # إرسال الرسالة إلى Telegram
        telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        for chat_id in CHAT_IDS:
            payload = {
                "chat_id": chat_id,
                "text": f"🚨 *New Alert Received:*\n{message}",
                "parse_mode": "Markdown"
            }
            res = requests.post(telegram_url, json=payload)
            print(f"📤 Sent to {chat_id}, response: {res.status_code}")

        return '✅ Message processed and sent to Telegram!'
    except Exception as e:
        print("❌ Error occurred:", e)
        return f"❌ Error: {e}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
