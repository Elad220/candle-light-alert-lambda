import os
import requests
import datetime
import logging

BOT_TOKEN = os.environ['BOT_TOKEN']
BOT_CHATID = os.environ['BOT_CHATID']
URL = 'https://www.hebcal.com/shabbat?cfg=json&geonameid=293397&M=on'

logging.basicConfig(level=logging.INFO)

def send_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    params = {'chat_id': BOT_CHATID, 'text': message}
    response = requests.post(url, data=params)
    response.raise_for_status()
    return response.json()

def get_candle_time():
    try:
        response = requests.get(URL)
        response.raise_for_status()
        json_response = response.json()
        for item in json_response['items']:
            if item['category'] == 'candles':
                candle_time = item['date']
                break
        candle_time = (candle_time.split('+')[0])
        return datetime.datetime.strptime(candle_time, '%Y-%m-%dT%H:%M:%S').time()
    except requests.exceptions.HTTPError as errh:
        logging.error(f"HTTP Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        logging.error(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        logging.error(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        logging.error(f"Something went wrong: {err}")
    return None

def lambda_handler(event, context):
    candle_time = get_candle_time()
    if candle_time:
        send_message(f"The candle lighting time for today is {candle_time}.")
    else:
        logging.error("No candle lighting time found.")
