from ..models import Topic
from ..models.Command1Arg import Command1Arg
from ..utils import dict_to_markdown


class InfoCmd(Command1Arg):
    cmd = '/info'

    def with_argument(self):
        try:
            topic = self.chat.subscribed_topics.get(code=self.the_argument)
            text = dict_to_markdown(
                topic.info(humanize=True),
                (('code', 'Code'),
                 ('subscribers_count', 'Subscribers'),
                 ('last_publish', 'Last publish'),
                 ('created_at', 'Created at'))
            )
        except Topic.DoesNotExist:
            text = ("Sorry, I could't find the topic `{topic_code}` in "
                    "your subscriptions.".format(topic_code=self.the_argument))
        return text

    def without_argument(self):
        keyboard = self.chat.subscribed_as_keyboard()
        if keyboard:
            return {
                'text': "Ok, now send me the TopicCode",
                'reply_markup': {
                    'keyboard': keyboard,
                    'resize_keyboard': True,
                    'one_time_keyboard': True,
                }
            }
        else:
            return ("Sorry, you don't have any topic yet.\n"
                    "Send me /new to create a Topic.")
