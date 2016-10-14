from celery import shared_task

from bot.commands import NewCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.new',
    bind=True,
    max_retries=6,
)
def new(self, update):
    try:
        return NewCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
