from flask import Flask, request
import requests

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
    return "✅ Telegram Bot is running!"

@app.route('/webhook', methods=['POST'])
def alert():
    data = request.get_json(force=True, silent=True)
    message = data.get('message') or str(data)
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    
    for chat_id in CHAT_IDS:
        payload = {
            "chat_id": chat_id,
            "text": message
        }
        requests.post(telegram_url, json=payload)
    
    return '✅ Message sent to all recipients!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
