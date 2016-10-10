from ..models.Command0Arg import Command0Arg


class SubscribeCmd(Command0Arg):
    cmd = '/subscribe'

    def without_argument(self):
        return ''.join(["You send me ", self.cmd])
