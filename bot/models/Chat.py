from django.db import models
import json


class Chat(models.Model):
    CHAT_TYPES = (
        ('private', 'Private'),
        ('group', 'Group'),
        ('supergroup', 'Supergroup'),
        ('channel', 'Channel'),
    )

    id = models.BigIntegerField(
        verbose_name='Chat ID',
        primary_key=True,
        help_text='Unique identifier for this chat',
    )
    type = models.CharField(
        verbose_name='Type',
        max_length=10,
        choices=CHAT_TYPES,
        help_text='Type of chat',
    )
    title = models.CharField(
        verbose_name='Title',
        max_length=128,
        blank=True,
        null=True,
        help_text='Title, for supergroups, channels and group chats',
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=128,
        blank=True,
        null=True,
        help_text=('Username, for private chats, supergroups '
                   'and channels if available'),
    )
    first_name = models.CharField(
        verbose_name='First name',
        max_length=128,
        blank=True,
        null=True,
        help_text='First name of the other party in a private chat',
    )
    last_name = models.CharField(
        verbose_name='Last name',
        max_length=128,
        blank=True,
        null=True,
        help_text='Last name of the other party in a private chat',
    )
    state = models.CharField(
        verbose_name='State',
        max_length=128,
        default='root',
        help_text=("A short memory, to store the last command if the command "
                   "have a flow with more than one message"),
    )

    @property
    def get_state_json(self):
        return json.loads(self.state)

    @property
    def set_state_json(self, payload):
        self.state = json.dumps(payload)
        return self.state
