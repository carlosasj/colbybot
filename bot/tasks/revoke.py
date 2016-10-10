from celery import shared_task

from bot.commands import RevokeCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.revoke',
    bind=True,
    max_retries=6,
)
def revoke(self, update):
    try:
        return RevokeCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
