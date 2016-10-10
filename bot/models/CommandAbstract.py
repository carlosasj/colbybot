from abc import ABC, abstractmethod

from emoji import emojize

from bot.models import Chat
from ..tasks.generic_send import send_message


class CommandAbstract(ABC):
    cmd = None

    def __init__(self, update):
        self.update = update
        self.chat = Chat.objects.get(id=update['message']['chat']["id"])

    def beautify_and_send(self, msg):
        if type(msg) is str:
            msg_ = {'text': msg}
        elif type(msg) is not dict:
            raise TypeError('"msg" must be "str" or "dict"')
        elif 'text' not in msg:
            raise KeyError('"msg" must contain at least "text" key')
        else:
            msg_ = msg

        if 'parse_mode' not in msg_:
            msg_['parse_mode'] = 'Markdown'
        if msg_['parse_mode'] == 'Markdown':
            msg_['text'] = emojize(msg_['text'])
        if 'chat_id' not in msg_:
            msg_['chat_id'] = self.chat.id
        if self.chat.state == 'root' and 'reply_markup' not in msg_:
            msg_['reply_markup'] = {'hide_keyboard': True}
        send_message.delay(msg_)

    @abstractmethod
    def execute(self):
        pass
