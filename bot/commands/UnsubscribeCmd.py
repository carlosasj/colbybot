from bot.messages_commom import NOT_FOUND_YOUR_SUBSC
from ..models.Command1Arg import Command1Arg


class UnsubscribeCmd(Command1Arg):
    cmd = '/unsubscribe'

    def with_argument(self):
        if self.chat.owned_topics.filter(code=self.the_argument).exists():
            return ("Sorry, you can't unsubscribe a topic you own (but you "
                    "can delete it, if you want)")

        elif self.chat.subscribed_topics.filter(
                code=self.the_argument).exists():
            topic = self.chat.owned_topics.get(code=self.the_argument)
            topic.subscribers.remove(self.chat)
            return "You'll not receive notifications from this topic anymore"
        else:
            return NOT_FOUND_YOUR_SUBSC.format(topic_code=self.the_argument)

    def without_argument(self):
        return self.ask_for_topic_code()