from django.conf.urls import url
from ..views import telegram_frontend as views


urlpatterns = [
    url(r'^$', views.parse_commands),
    url(r'^status/$', views.status),
]
