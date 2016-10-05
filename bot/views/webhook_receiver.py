from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from ..models import Topic


@require_http_methods(["GET", "POST"])
def endpoint_public(request, code, secret):
    topic = get_object_or_404(Topic, code=code, secret=secret)

    if request.method == 'POST':
        return endpoint_public_post(request, topic)
    else:
        return endpoint_public_get(request, topic)


def endpoint_public_get(request, topic):
    data = {
        'code': topic.code,
        'subscribers_count': topic.subscribers.count(),
        'last_publish': topic.last_publish,
        'created_at': topic.created_at,
    }
    return JsonResponse(data, status=200)


def endpoint_public_post(request, topic):
    pass
