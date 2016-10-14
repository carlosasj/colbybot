import json

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..parsers import urlparams, payload
from ..serializers import TopicSerializer
from ..models import Topic


class TopicWebhook(APIView):

    def get_object(self, code, secret):
        return get_object_or_404(Topic, code=code, secret=secret)

    def get(self, request, code, secret):
        topic = self.get_object(code, secret)
        serializer = TopicSerializer(topic)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, code, secret):
        topic = self.get_object(code, secret)
        params = urlparams.parse(request.GET)
        text = payload.parse(params, json.loads(request.body.decode("utf-8")))
        text = "".join([text, "\n\n*Topic:* `", str(topic.code), "`"])
        return HttpResponse(text, status=status.HTTP_200_OK)
