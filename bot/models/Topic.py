from django.db import models, IntegrityError
from django.utils.timezone import now
from ..utils import randomstr


class TopicManager(models.Manager):
    def generate_new(self, owner):
        try_again = True
        count = 0
        code = randomstr()
        secret = randomstr(16)

        while try_again:
            try:
                topic = self.create(code=code, secret=secret, owner=owner)
                try_again = False
            except IntegrityError:
                count = min(count+1, 64)
                code = randomstr(max(6, count))

        topic.subscribers.add(owner)
        return topic


class Topic(models.Model):
    code = models.CharField(
        verbose_name='Code',
        max_length=64,
        unique=True
    )
    secret = models.CharField(
        verbose_name='Secret',
        max_length=16,
    )
    subscribers = models.ManyToManyField(
        'bot.Chat',
        verbose_name='Subscribers',
        related_name='subscribed_topic'
    )
    last_publish = models.DateTimeField(
        verbose_name='Last publish',
        default=now,
    )
    created_at = models.DateTimeField(
        verbose_name='Created at',
        default=now,
    )
    owner = models.ForeignKey(
        'bot.Chat',
        verbose_name='Owner',
        related_name='owned_topics'
    )

    objects = TopicManager()
