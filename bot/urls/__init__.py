from django.conf.urls import url, include


urlpatterns = [
    url(r'^parse_commands/', include('bot.urls.telegram_frontend')),
]
