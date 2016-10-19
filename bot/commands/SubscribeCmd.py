from ..models.Command1Arg import Command1Arg
from ..models import Topic


class SubscribeCmd(Command1Arg):
    cmd = '/subscribe'

    def with_argument(self):
        if self.chat.subscribed_topics.filter(code=self.the_argument).exists():
            return "You are already subscribed to this topic"

        elif Topic.objects.filter(code=self.the_argument).exists():
            topic = Topic.objects.get(code=self.the_argument)
            topic.subscribers.add(self.chat)
            return "Now you will receive notifications from this Topic!"

        else:
            return ("Sorry, I could't find the topic `{topic_code}`"
                    .format(topic_code=self.the_argument))

    def without_argument(self):
        return "Ok, now send me the TopicCode to subscribe"
