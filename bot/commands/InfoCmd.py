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
            return {
                'text': text,
                'reply_markup': {
                    'inline_keyboard': [
                        [
                            {'text': "Revoke", 'callback_data': "CB_REVOKE {}".format(topic.code)},
                            {'text': "Delete", 'callback_data': "CB_DELETE {}".format(topic.code)},
                        ]
                    ]
                }
            }
        except Topic.DoesNotExist:
            text = ("Sorry, I could't find the topic `{topic_code}` in "
                    "your subscriptions.".format(topic_code=self.the_argument))
            return text

    def without_argument(self):
        return self.ask_for_topic_code()
