from time import sleep
import logging

import requests
import os

offset = 432604897
BASE_URL = 'https://api.telegram.org/bot'
TOKEN = os.getenv('TOKEN')
BOT_URL = os.getenv('BOT_URL')


def api_path(path):
    return ''.join([BASE_URL, TOKEN, '/', path])


def skip_initial():
    global offset
    size = 100
    while size == 100:
        data = {"offset": offset}
        r = requests.get(api_path('getUpdates'), params=data)
        try:
            assert r.status_code == 200
            back = r.json()
            assert back['ok'] is True
            size = len(back['result'])
            if size > 0:
                offset = max(back['result'],
                             key=lambda x: x['update_id']
                             )['update_id'] + 1
        except AssertionError:
            sleep(1.5)


def main():
    global offset
    logging.critical("POOL UP \o/")
    # Pula todos os updates até não ter mais nenhum
    skip_initial()
    logging.critical("Dados iniciais consumidos")

    while True:
        sleep(1.5)

        delivered = False

        data = {"offset": offset, "limit": 1}
        r = requests.get(api_path('getUpdates'), params=data)
        if (r.status_code != 200 or
            r.json()['ok'] is not True or
                len(r.json()['result']) != 1):
            continue
        update = r.json()['result'][0]
        offset = update['update_id'] + 1

        while not delivered:
            r = requests.post(BOT_URL, json=update)
            if r.status_code == 200:
                delivered = True
                logging.critical([offset-1, 'OK'])
            else:
                logging.critical([offset-1, 'FAIL'])
                sleep(1.5)

if '__main__' == __name__:
    log_level = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL,
    }
    logging.basicConfig(level=log_level[os.getenv('LOG_LEVEL', 'INFO')])
    main()
