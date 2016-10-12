from abc import abstractmethod

from ..messages_commom import EMPTY
from ..models.CommandAbstract import CommandAbstract


class Command1Arg(CommandAbstract):
    cmd = None

    def __init__(self, update):
        super(Command1Arg, self).__init__(update)
        self.the_argument = self.update['validations']['the_argument']

    @abstractmethod
    def with_argument(self):
        pass

    @abstractmethod
    def without_argument(self):
        pass

    def ask_for_topic_code(self):
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
            return EMPTY

    def execute(self):
        if self.the_argument:
            msg = self.with_argument()
            if self.update['validations']['contains_command']:
                self.chat.state = 'root'
                self.chat.save()
        else:
            msg = self.without_argument()
            self.chat.set_state_json({'last_cmd': self.cmd})
            self.chat.save()

        self.beautify_and_send(msg)
        return 0
