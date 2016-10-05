from celery import shared_task

from bot.utils import gen_delay
from .generic_send import send_message


@shared_task(
    name='cmd.revoke',
    bind=True,
    max_retries=6,
)
def revoke(self, update):
    try:
        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": "You send me /revoke",
        }
        send_message.delay(msg)
        return 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
