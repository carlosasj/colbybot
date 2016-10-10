from celery import shared_task

from bot.commands import DocsCmd
from bot.utils import gen_delay


@shared_task(
    name='cmd.docs',
    bind=True,
    max_retries=6,
)
def docs(self, update):
    try:
        return DocsCmd(update).execute()
    except Exception as exc:
        raise self.retry(exc=exc, countdown=gen_delay(self))
