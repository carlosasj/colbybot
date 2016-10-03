from celery import shared_task

from bot.utils import gen_delay
from .generic_send import send_message

GREETINGS = """*Welcome to Colby Bot!*

TL;DR : /new

Are you tired from receiving e-mails from your CI Provider or your \
HealthCheck service?
Are you tired from configuring those services?
Don't be anymore. I'm here for your services!

If you want to create a new topic to publish, send me /new

If you already have a TopicCode and want to receive these notifications, \
send me /subscribe \[TopicCode]
(i.e. /subscribe btc0l5)

Well... Welcome to Colby Bot!
I'm glad you chose my services.

```text
     __   auf
(___()'`;    auf
/,    /`
\\\\"--\\\\
```
"""


@shared_task(
    name='cmd.start',
    bind=True,
    max_retries=16,
)
def start(self, update):
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