import os
import requests
from datetime import datetime
import logging
import json

BOT_TOKEN = os.environ['BOT_TOKEN']

logging.basicConfig(level=logging.INFO)

def send_message(message, chat_ids):
    for chat_id in chat_ids:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        params = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=params)
        response.raise_for_status()
        logging.info(f"Message sent: {message} to chat_id: {chat_id}")

def get_chatids():
    chat_ids = os.environ['BOT_CHATID']
    return json.loads(chat_ids)


def lambda_handler(event, context):
    candle_time = event["candle_time"]
    mins = event["scheduled_for"]
    candle_time = datetime.fromisoformat(candle_time)
    message = f'Candle lighting time is in {mins} minutes at {candle_time.time()}'
    logging.info(f"Message: {message}")
    chat_ids = get_chatids()
    send_message(message, chat_ids)

