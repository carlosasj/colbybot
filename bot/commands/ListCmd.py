from ..messages_commom import EMPTY
from ..models.Command0Arg import Command0Arg


text = """Here are the topics you subscribed:

{topics}

:crown: = you own this repo
"""


def format_topic_list(topics, chat=None):
    if chat:
        id_ = chat.id
        topics_txt = [''.join([str(i + 1), '. ', topic.code,
                               ' :crown:' if topic.owner_id == id_ else ''])
                      for i, topic in enumerate(topics)]

    else:
        topics_txt = [''.join([str(i + 1), '. ', topic.code])
                      for i, topic in enumerate(topics)]

    return '\n'.join(topics_txt)


class ListCmd(Command0Arg):
    cmd = '/list'

    def without_argument(self):
        topics = self.chat.subscribed_topics.all()
        if topics:
            topics_txt = format_topic_list(topics, self.chat)
            return text.format(topics=topics_txt)
        else:
            return EMPTY
