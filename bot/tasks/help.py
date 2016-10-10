from celery import shared_task

from bot.commands import HelpCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.help',
    bind=True,
    max_retries=6,
)
def help_(self, update):
    try:
        return HelpCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
