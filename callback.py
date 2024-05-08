from flask import Flask, request, jsonify
import requests
import json
from bs4 import BeautifulSoup
import re

app = Flask(__name__)

# LINE Channel Access Token
LINE_CHANNEL_ACCESS_TOKEN = "Your_LINE_Channel_Access_Token"

# LINE API URL
LINE_API_URL = "https://api.line.me/v2/bot/message/reply"

# Dummy data for demonstration
house_data = [
    {"name": "House A", "price": "$100,000", "location": "City X"},
    {"name": "House B", "price": "$150,000", "location": "City Y"},
    {"name": "House C", "price": "$200,000", "location": "City Z"}
]

# Handle LINE messages
@app.route("/callback", methods=["POST"])
def callback():
    payload = request.get_data(as_text=True)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + LINE_CHANNEL_ACCESS_TOKEN
    }
    reply_to_line(payload, headers)
    return "OK", 200

# Reply to LINE messages
def reply_to_line(payload, headers):
    data = json.loads(payload)
    for event in data["events"]:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_id = event["source"]["userId"]
            message_text = event["message"]["text"]
            if "物件" in message_text:  # If the user asks about houses
                reply_text = get_house_info()
            elif "聯絡" in message_text:  # If the user wants to contact
                reply_text = "請填寫聯絡資訊表單：[連結]"
            else:
                reply_text = "請問有什麼可以幫助您的嗎？"
            send_reply_message(user_id, reply_text, headers)

# Get house information
def get_house_info():
    house_info = ""
    for house in house_data:
        house_info += f"{house['name']} - {house['price']} - {house['location']}\n"
    return house_info

# Send reply message to user
def send_reply_message(user_id, reply_text, headers):
    payload = {
        "replyToken": user_id,
        "messages": [{"type": "text", "text": reply_text}]
    }
    requests.post(LINE_API_URL, headers=headers, data=json.dumps(payload))

# Main function
if __name__ == "__main__":
    app.run(debug=True)
