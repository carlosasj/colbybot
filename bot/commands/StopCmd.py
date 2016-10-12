from ..models.Command0Arg import Command0Arg


EXPLAIN = ("This command erases all your data from the server, but to do so, "
           "first you have to /unsubscribe and /delete all your Topics")


class StopCmd(Command0Arg):
    cmd = '/stop'

    def without_argument(self):
        if self.chat.subscribed_topics.exists():
            return EXPLAIN
        else:
            data = {
                'chat_id': self.chat.id,
                'text': "Your data has been deleted. Bye.",
                'reply_markup': {'hide_keyboard': True}
            }
            self.chat.delete()
            return data
