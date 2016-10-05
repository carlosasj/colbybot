from django.conf.urls import url
from ..views import telegram_frontend as views


urlpatterns = [
    url(r'^parse_commands/status/$', views.status),
    url(r'^parse_commands/$', views.parse_commands),
]
