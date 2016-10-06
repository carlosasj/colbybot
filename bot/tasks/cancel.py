from celery import shared_task

from bot.utils import gen_delay
from .generic_send import send_message
from ..models import Chat


@shared_task(
    name='cmd.cancel',
    bind=True,
    max_retries=6,
)
def cancel(self, update, argument=None):
    try:
        chat = Chat.objects.get(id=update['message']['chat']["id"])
        if chat.state == 'root':
            text = "Okay... nothing to cancel..."
        else:
            chat.state = "root"
            chat.save()
            text = "I'll forget about that, then."
        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": text,
        }
        send_message.delay(msg)
        return 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
