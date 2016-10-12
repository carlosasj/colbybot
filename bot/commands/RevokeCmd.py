from bot.messages_commom import ASK_THE_OWNER, NOT_FOUND_YOUR_SUBSC
from ..models.Command1Arg import Command1Arg


TEXT = """I'd generate a new secret to your topic. Please, update the new \
URL in all services who publish in this endpoint.

Here is the new URL:
{webhook_endpoint}"""


class RevokeCmd(Command1Arg):
    cmd = '/revoke'

    def with_argument(self):
        if self.chat.owned_topics.filter(code=self.the_argument).exists():
            topic = self.chat.owned_topics.get(code=self.the_argument)
            topic.revoke()
            topic.refresh_from_db()
            return TEXT.format(webhook_endpoint=topic.webhook_endpoint)

        elif self.chat.subscribed_topics.filter(
                code=self.the_argument).exists():
            return ASK_THE_OWNER
        else:
            return NOT_FOUND_YOUR_SUBSC.format(topic_code=self.the_argument)

    def without_argument(self):
        return self.ask_for_topic_code()
