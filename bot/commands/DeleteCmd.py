from ..models.Command0Arg import Command0Arg


class DeleteCmd(Command0Arg):
    cmd = '/delete'

    def without_argument(self):
        return ''.join(["You send me ", self.cmd])
