from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class OHQueueSerializer(serializers.ModelSerializer):
    question_contents = serializers.ReadOnlyField()
    number_questions = serializers.ReadOnlyField()
    class Meta:
        model = models.OHQueue
        read_only_fields = ('average_wait_time', 'number_questions')
        fields = ('name', 'average_wait_time', 'is_open_extended', 'is_closed', 'is_in_time', 'question_contents', 'number_questions')
    def create(self, validated_data):
        ohqueue =  models.OHQueue.objects.create(**validated_data)
        return ohqueue