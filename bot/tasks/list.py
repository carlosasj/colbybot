from celery import shared_task

from bot.utils import gen_delay
from .generic_send import send_message
from ..models import Chat

crown = '\U0001F451'
_crown = ' \U0001F451'

text = """Here are the topics you subscribed:

{topics}

{crown} = you own this repo
"""


@shared_task(
    name='cmd.list',
    bind=True,
    max_retries=6,
)
def list_(self, update):
    try:
        chat = Chat.objects.get(id=update['message']['chat']["id"])
        topics = chat.subscribed_topics.all()
        topics_txt = [''.join(
            [str(i+1), '. ', topic.code,
             _crown if topic.owner_id == chat.id else ''
             ]) for i, topic in enumerate(topics)]
        topics_txt = '\n'.join(topics_txt)
        text_ = text.format(topics=topics_txt, crown=crown)

        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": text_,
        }
        send_message.delay(msg)
        return 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
