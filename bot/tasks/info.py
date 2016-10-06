from celery import shared_task
from celery.utils.log import get_task_logger

from bot.models import Chat
from bot.models import Topic
from bot.utils import gen_delay, dict_to_markdown
from .generic_send import send_message

logger = get_task_logger(__name__)


@shared_task(
    name='cmd.info',
    bind=True,
    max_retries=6,
)
def info(self, update, argument=None):
    try:
        chat = Chat.objects.get(id=update['message']['chat']["id"])
        reply_markup = {}

        if argument:
            try:
                topic = chat.subscribed_topics.get(code=argument)
                text = dict_to_markdown(
                    topic.info(humanize=True),
                    (('code', 'Code'),
                     ('subscribers_count', 'Subscribers'),
                     ('last_publish', 'Last publish'),
                     ('created_at', 'Created at'))
                )
                if not update['validations']['contains_command']:
                    chat.state = 'root'
                    chat.save()
            except Topic.DoesNotExist:
                text = ("Sorry, I could't find the topic `{topic_code}` in "
                        "your subscriptions.")
        else:
            chat.set_state_json({'last_cmd': '/info'})
            chat.save()
            text = "Ok, now send me the TopicCode"
            reply_markup = {
                'keyboard': chat.subscribed_as_keyboard(),
                'resize_keyboard': True,
                'one_time_keyboard': True,
            }

        msg = {
            "chat_id": update['message']['chat']["id"],
            "text": text,
            "parse_mode": "Markdown",
        }
        if reply_markup:
            msg['reply_markup'] = reply_markup
        send_message.delay(msg)
        return 0
    except Exception as exc:
        import traceback
        logger.exception(traceback.format_exc())
        raise self.retry(exc=exc, countdown=gen_delay(self))
