import os
import requests
from flask import Flask, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

TG_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def send_message(chat_id, text):
    requests.post(
        f"{TG_API}/sendMessage",
        json={"chat_id": chat_id, "text": text}
    )

@app.route("/", methods=["GET"])
def home():
    return "bot is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        try:
            response = client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {"role": "system", "content": "Ты полезный ассистент."},
                    {"role": "user", "content": text}
                ]
            )

            answer = response.choices[0].message.content

        except Exception as e:
            answer = "AI ошибка"

        send_message(chat_id, answer)

    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)