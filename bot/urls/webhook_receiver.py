from django.conf.urls import url
from ..views import webhook_receiver as views


urlpatterns = [
    url(r'^(?P<code>[0-9a-zA-Z\-]+)_(?P<secret>[0-9a-zA-Z\-]+)/$',
        views.endpoint_public, name='publish_endpoint'),
]
