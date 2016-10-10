from rest_framework import serializers
from ..models import Topic


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            'code',
            'subscribers_count',
            'last_publish',
            'created_at',
        )
        read_only_fields = fields


class TopicHumanizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = (
            'code',
            'subscribers_count',
            'last_publish_humanize',
            'created_at_humanize',
        )
        read_only_fields = fields
