import traceback
import urllib.parse

import requests


def send_to_telegram(token_info, message):
    try:
        token = token_info['token']
        user_id = token_info['user_id']
        message = urllib.parse.quote(message)
        url = f'https://api.telegram.org/bot{token}/sendMessage?chat_id={user_id}&text={message}'
        resp = requests.get(url)
        print('Notify code: ', resp.status_code)
    except Exception as e:
        print('Telegram notify error: ' + str(e))
        print(traceback.format_exc())
