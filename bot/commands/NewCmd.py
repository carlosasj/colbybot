from django.conf import settings
from django.urls import reverse

from ..models import Topic
from ..models.Command0Arg import Command0Arg


TEXT = """Great! Now you have a new topic!

You can send `HTTP POST` requests to:
`{webhook_endpoint}`

If you want more people receiving the notifications, send them this TopicCode:
`{topic_code}`

I've already subscribed you to this topic.
"""


class NewCmd(Command0Arg):
    cmd = '/new'

    def without_argument(self):
        topic = Topic.objects.generate_new(self.chat)

        return TEXT.format(webhook_endpoint=topic.webhook_endpoint,
                           topic_code=topic.code)
