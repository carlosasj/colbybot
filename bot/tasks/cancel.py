from celery import shared_task

from ..commands import CancelCmd
from ..utils import gen_delay


@shared_task(
    name='cmd.cancel',
    bind=True,
    max_retries=6,
)
def cancel(self, update):
    try:
        return CancelCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
