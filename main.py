import json
import random
import time
import os
import traceback

import requests
from requests_html import HTML

from notify import send_to_telegram

TOKEN_LIST = json.loads(os.getenv('TOKEN_LIST'))
TG_CONFIG = json.loads(os.getenv('TG_CONFIG'))

if __name__ == '__main__':
    try:
        for token in TOKEN_LIST:
            research = requests.get(
                'https://insights.phoenix.global/research',
                headers={'cookie': f'token={token}'},
            )

            html = HTML(html=research.text)
            for element in html.find('.slim-item'):
                r_id = element.find('a')[0].attrs['href'].split('-')[-1]
                rating_payload = {'report_id': r_id, 'rating_value': random.randint(4, 5)}
                temp = requests.post(
                    'https://api.phoenix.global/api/v1/report-rating/',
                    headers={'authorization': f'Token {token}'},
                    json=rating_payload,
                )
                print(temp.json())
                time.sleep(2)
        message = f'Rating successful with {len(TOKEN_LIST)} accounts.'
    except Exception as e:
        print('Rating error: ' + str(e))
        error_traceback = traceback.format_exc()
        print(error_traceback)
        message = 'Error when rating: \n' + error_traceback

    send_to_telegram(TG_CONFIG, message)
