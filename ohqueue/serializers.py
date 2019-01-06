from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class OHQueueSerializer(serializers.ModelSerializer):
    question_contents = serializers.ReadOnlyField()
    wait_time = serializers.ReadOnlyField()
    class Meta:
        model = models.OHQueue
        read_only_fields = ('wait_time')
        fields = ('name', 'is_open_extended', 'is_closed', 'is_in_time', 'question_contents', 'wait_time')
    def create(self, validated_data):
        ohqueue =  models.OHQueue.objects.create(**validated_data)
        return ohqueue