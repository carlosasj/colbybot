from celery import shared_task

from bot.utils import gen_delay
from .generic_send import send_message


@shared_task(
    name='cmd.start',
    bind=True,
    max_retries=16,
)
def new(self, update):
    try:
        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": GREETINGS,
            "parse_mode": "Markdown",
        }
        send_message.delay(msg)
        return 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))