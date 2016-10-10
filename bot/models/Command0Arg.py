from abc import abstractmethod

from bot.models.CommandAbstract import CommandAbstract


class Command0Arg(CommandAbstract):

    @abstractmethod
    def without_argument(self):
        pass

    def execute(self):
        msg = self.without_argument()
        self.chat.state = 'root'
        self.chat.save()
        self.beautify_and_send(msg)
        return 0
