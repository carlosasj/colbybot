from functools import lru_cache
from .Chat import Chat


class MessageEntity:
    def __init__(self, body):
        keys = ['type', 'offset', 'length', 'url', 'user']
        for key in keys:
            if key in body:
                setattr(self, key, body[key])


def to_messageentity_array(body):
    return sorted([MessageEntity(item) for item in body],
                  key=lambda ent: ent.offset)


class Message:
    def __init__(self, body):

        self.is_reply = 'reply_to_message' in body

        self.is_forward = any(key in body for key in ['forward_from',
                                                      'forward_from_chat',
                                                      'forward_date'])
        keys = [
            'message_id', 'date', 'chat',
            'text', 'entities', 'audio', 'document', 'photo', 'sticker',
            'video', 'voice', 'caption', 'contact', 'location', 'venue',
            'new_chat_member', 'left_chat_member', 'new_chat_title',
            'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
            'supergroup_chat_created', 'channel_chat_created',
            'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
            'forward_from', 'forward_from_chat', 'forward_date']
        for key in keys:
            if key in body:
                setattr(self, key, body[key])
        if hasattr(self, 'entities'):
            self.entities = to_messageentity_array(self.entities)

    @property
    @lru_cache()
    def contains_command(self):
        return (hasattr(self, 'entities') and
                any(ent.type == 'bot_command' for ent in self.entities))

    @property
    def contains_single_command(self):
        return len([ent.type == 'bot_command' for ent in self.entities]) == 1

    @property
    def startswith_command(self):
        return (self.contains_command and
                self.entities[0].type == 'bot_command' and
                self.entities[0].offset == 0)

    @property
    @lru_cache()
    def the_command(self):
        if self.contains_command:
            entity = next(ent for ent in self.entities
                          if ent.type == 'bot_command')
            return (self.text[entity.offset:(entity.offset+entity.length)]
                    .split('@', 1)[0])
        else:
            return None

    @property
    @lru_cache()
    def the_argument(self):
        cmd = self.the_command
        if cmd is None:
            arg = self.text.strip().split(' ', 1)
        else:
            entity = next(ent for ent in self.entities
                          if ent.type == 'bot_command')
            arg = (self.text[(entity.offset+entity.length):]
                   .strip().split(' ', 1))

        return arg[0] if len(arg) > 0 and arg[0] else None

    def is_valid_command(self, commands):
        cmd = self.the_command
        if cmd is None:
            return False
        else:
            return cmd in commands

    @property
    def chat_model(self):
        if not hasattr(self, '_chat_model'):
            self._chat_model = Chat.objects.get(id=self.chat['id'])
        return self._chat_model
