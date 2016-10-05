from celery import shared_task
import requests
from ..utils import api_path, gen_delay
import logging


@shared_task(
    name='generic.send',
    bind=True,
    max_retries=6,
    rate_limit='30/s'
)
def send_message(self, message):
    r = requests.post(api_path('sendMessage'), json=message)
    logging.info({"message": message, "status": r.status_code})
    if r.status_code == 200:
        return 0
    else:
        raise self.retry(
            exc=Exception('Error while sending message'),
            countdown=gen_delay(self)
        )
