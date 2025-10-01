from flask import Flask, request
import requests
import os

app = Flask(__name__)
LINE_TOKEN = os.getenv("LINE_TOKEN")

@app.route('/webhook', methods=['POST', 'GET'])
def webhook():
    if request.method == 'GET':
        return 'OK', 200
    
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
    url = 'https://api.line.me/v2/bot/message/reply'
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
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)