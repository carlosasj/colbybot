from celery import shared_task
from django.conf import settings
from django.urls import reverse

from bot.utils import gen_delay
from .generic_send import send_message
from ..models import Topic, Chat

TEXT = """Great! Now you have a new topic!

You can send `HTTP POST` requests to:
`{webhook_endpoint}`

If you want more people receiving the notifications, send them this TopicCode:
`{topic_code}`

I've already subscribed you to this topic.
"""


@shared_task(
    name='cmd.new',
    bind=True,
    max_retries=6,
)
def new(self, update, argument=None):
    try:
        chat = Chat.objects.get(id=update['message']['chat']['id'])
        topic = Topic.objects.generate_new(chat)
        webhook_endpoint = ''.join([
            settings.DOMAIN,
            reverse('publish_endpoint',
                    kwargs={"code": topic.code, "secret": topic.secret})
        ])

        chat.state = 'root'
        chat.save()

        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": TEXT.format(webhook_endpoint=webhook_endpoint,
                                topic_code=topic.code),
            "parse_mode": "Markdown",
        }
        send_message.delay(msg)
        return 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))