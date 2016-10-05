from celery import shared_task

from bot.utils import gen_delay
from .generic_send import send_message

TEXT = """Here follows ALL the supported commands:

/cancel - Cancel an action at any time
/start - Start the chat with me!
/help - Show this message
/docs - Get more info about how to format the message

/new - Create a new topic
/subscribe \[TopicCode] - Subscribe to a Topic
/unsubscribe \[TopicCode] - Unsubscribe a Topic
/info \[TopicCode] - Get some info and stats from some topic
/revoke \[TopicCode] - Change the Secret from a topic you own
/list - List all subscribed topics
/delete \[TopicCode] - Delete a topic you own

/stop - Remove every information about you from the server

-----
All commands with \[TopicCode] can be used in two ways:
1. Single message: */command [TopicCode]*
2. Two messages: First */command*, then *[TopicCode]*

The /stop command will require you to unsubscribe to all topics and delete \
all topics you are the owner.
"""


@shared_task(
    name='cmd.help',
    bind=True,
    max_retries=6,
)
def help_(self, update):
    try:
        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": TEXT,
            "parse_mode": "Markdown",
        }
        send_message.delay(msg)
        return 0
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
