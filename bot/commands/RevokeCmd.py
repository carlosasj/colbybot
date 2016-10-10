from ..models.Command0Arg import Command0Arg


class RevokeCmd(Command0Arg):
    cmd = '/revoke'

    def without_argument(self):
        return ''.join(["You send me ", self.cmd])
