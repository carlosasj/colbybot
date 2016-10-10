from celery import shared_task

from bot.commands import UnsubscribeCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.unsubscribe',
    bind=True,
    max_retries=6,
)
def unsubscribe(self, update):
    try:
        return UnsubscribeCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
