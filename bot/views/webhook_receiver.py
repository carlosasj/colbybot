import json

from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from ..parsers import urlparams, payload
from ..serializers import TopicSerializer
from ..models import Topic
from ..tasks.generic_send import send_message


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

        for chat in topic.subscribers.all():
            msg = {
                "chat_id": chat.id,
                "text": text,
                "parse_mode": "Markdown",
            }
            send_message.delay(msg)

        return Response({"details": "ok"}, status=status.HTTP_200_OK)
