from celery import shared_task

from bot.commands import ListCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.list',
    bind=True,
    max_retries=6,
)
def list_(self, update):
    try:
        return ListCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
