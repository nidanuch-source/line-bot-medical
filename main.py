from flask import Flask, request
import requests

app = Flask(__name__)

# ใส่ Channel Access Token ของคุณ
LINE_TOKEN = "O1AtOSiIRBkef/1YRTMZJDrRIjjwo87PfgOpSW055sWQz7vW0jdxGapD1utVXKuK4IkgvSHPt9lyK+BV+OPB2ssQEtmkq//1Miar3GvqzKqthJk7+o6gYhF2c+hyCnPWxG6trisUPouZdcWXaDl2BQdB04t89/1O/w1cDnyilFU="

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    # รองรับการ verify จาก LINE (GET request)
    if request.method == 'GET':
        return 'OK', 200
    
    # ประมวลผลข้อความ (POST request)
    body = request.get_json()
    if not body or 'events' not in body:
        return 'OK', 200

    for event in body.get('events', []):
        if event['type'] == 'message' and event['message']['type'] == 'text':
            reply_token = event['replyToken']
            user_message = event['message']['text']
            reply_message(reply_token, f"คุณส่งมาว่า: {user_message}")
    
    return 'OK'

def reply_message(reply_token, text):
    url = 'https://api.line.me/v2/bot/message/reply'  # ลบช่องว่างแล้ว!
    headers = {
        'Authorization': f'Bearer {LINE_TOKEN}',
        'Content-Type': 'application/json'
    }
    data = {
        'replyToken': reply_token,
        'messages': [{'type': 'text', 'text': text}]
    }
    requests.post(url, headers=headers, json=data)

if __name__ == '__main__':
    app.run(debug=True)