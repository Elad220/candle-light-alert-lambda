import os
import requests
from datetime import datetime
import json
from aws_lambda_powertools import Logger

BOT_TOKEN = os.environ['BOT_TOKEN']
logger = Logger()


def send_message(message, chat_ids):
    for chat_id in chat_ids:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        params = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=params)
        response.raise_for_status()
        logger.info(f"Message sent: {message} to chat_id: {chat_id}")

def get_chatids():
    chat_ids = os.environ['BOT_CHATID']
    return json.loads(chat_ids)


def lambda_handler(event, context):
    candle_time = event["candle_time"]
    mins = event["scheduled_for"]
    candle_time = datetime.fromisoformat(candle_time)
    message = f'Candle lighting time is in {mins} minutes at {candle_time.time()}'
    logger.info(f"Message is: {message}")
    chat_ids = get_chatids()
    send_message(message, chat_ids)

