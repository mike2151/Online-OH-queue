from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class OHQueueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.OHQueue
        read_only_fields = ('questions', 'average_wait_time',)
        fields = ('name', 'questions', 'times_open', 'average_wait_time',)
    def create(self, validated_data):
        ohqueue =  models.OHQueue.objects.create(**validated_data)
        return ohqueue