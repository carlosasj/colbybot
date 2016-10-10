from ..models.Command0Arg import Command0Arg


class StopCmd(Command0Arg):
    cmd = '/stop'

    def without_argument(self):
        return ''.join(["You send me ", self.cmd])
