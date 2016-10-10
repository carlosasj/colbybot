from celery import shared_task

from bot.commands import SubscribeCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.subscribe',
    bind=True,
    max_retries=6,
)
def subscribe(self, update):
    try:
        return SubscribeCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
