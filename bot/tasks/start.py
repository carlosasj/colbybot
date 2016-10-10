from celery import shared_task
from celery.utils.log import get_task_logger

from bot.commands import StartCmd
from ..utils import gen_delay


logger = get_task_logger(__name__)


@shared_task(
    name='cmd.start',
    bind=True,
    max_retries=6,
)
def start(self, update):
    try:
        return StartCmd(update).execute()
    except Exception as exc:
        import traceback
        logger.exception(traceback.format_exc())
        raise self.retry(exc=exc, countdown=gen_delay(self))
