from ..models.Command0Arg import Command0Arg


class CancelCmd(Command0Arg):
    cmd = '/cancel'

    def without_argument(self):
        if self.chat.state == 'root':
            return "Okay... nothing to cancel..."
        else:
            return "I'll forget about that, then."
