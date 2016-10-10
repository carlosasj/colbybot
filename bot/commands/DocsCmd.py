from ..models.Command0Arg import Command0Arg


class DocsCmd(Command0Arg):
    cmd = '/docs'

    def without_argument(self):
        return ''.join(["You send me ", self.cmd])
