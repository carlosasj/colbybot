from bot.messages_commom import ASK_THE_OWNER, NOT_FOUND_YOUR_SUBSC
from ..models.Command1Arg import Command1Arg


class DeleteCmd(Command1Arg):
    cmd = '/delete'

    def with_argument(self):
        if self.chat.owned_topics.filter(code=self.the_argument).exists():
            # return "Pretend that I just deleted the topic :)"
            topic = self.chat.owned_topics.get(code=self.the_argument)
            topic.delete()
            return "I deleted the topic {topic_code}".format(
                topic_code=self.the_argument)

        elif self.chat.subscribed_topics.filter(
                code=self.the_argument).exists():
            return ASK_THE_OWNER
        else:
            return NOT_FOUND_YOUR_SUBSC.format(topic_code=self.the_argument)

    def without_argument(self):
        return self.ask_for_topic_code()
