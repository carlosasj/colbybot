from celery import shared_task

from bot.commands import StopCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.stop',
    bind=True,
    max_retries=6,
)
def stop(self, update):
    try:
        return StopCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
