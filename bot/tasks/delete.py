from celery import shared_task

from bot.commands import DeleteCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.delete',
    bind=True,
    max_retries=6,
)
def delete(self, update):
    try:
        return DeleteCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
