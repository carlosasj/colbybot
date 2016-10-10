from ..models.Command0Arg import Command0Arg


TEXT = """*Welcome to Colby Bot!*

TL;DR : /new

Are you tired from receiving e-mails from your CI Provider or your \
HealthCheck service?
Are you tired from configuring those services?
Don't be anymore. I'm here for your services!

If you want to create a new topic to publish, send me /new

If you already have a TopicCode and want to receive these notifications, \
send me /subscribe \[TopicCode]
(i.e. /subscribe btc0l5)

Well... Welcome to Colby Bot!
I'm glad you chose my services.

```text
     __   auf
(___()'`;    auf
/,    /`
\\\\"--\\\\
```
"""


class StartCmd(Command0Arg):
    cmd = '/help'

    def without_argument(self):
        return TEXT
