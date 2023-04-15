import os
import requests
from datetime import datetime
import json
from aws_lambda_powertools import Logger

BOT_TOKEN = os.environ['BOT_TOKEN']
logger = Logger(level="DEBUG")


def send_message(message, chat_ids):
    for chat_id in chat_ids:
        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        params = {'chat_id': chat_id, 'text': message}
        response = requests.post(url, data=params)
        response.raise_for_status()
        logger.debug(f"Message sent: {message} to chat_id: {chat_id}")

def get_chatids():
    chat_ids = os.environ['BOT_CHATID']
    logger.debug(f"chat_ids: {chat_ids}")
    return json.loads(chat_ids)


def lambda_handler(event, context):
    candle_time = event["candle_time"]
    mins = event["scheduled_for"]
    test_flag = event.get("test", False)
    test_prefix = "This is a test message!"
    candle_time = datetime.fromisoformat(candle_time)
    message = f'Candle lighting time is in {mins} minutes at {candle_time.hour}:{candle_time.minute}'
    if test_flag:
        logger.debug("test_flag is True, sending a test message")
        message = " ".join([test_prefix, message])
    logger.info(f"Message is: {message}")
    chat_ids = get_chatids()
    send_message(message, chat_ids)
    logger.info("Messages sent successfully!")
    return {"statusCode": 200, "body": "successfully sent reminder to all subscribers!"}

