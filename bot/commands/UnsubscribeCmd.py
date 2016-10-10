from ..models.Command0Arg import Command0Arg


class UnsubscribeCmd(Command0Arg):
    cmd = '/unsubscribe'

    def without_argument(self):
        return ''.join(["You send me ", self.cmd])
