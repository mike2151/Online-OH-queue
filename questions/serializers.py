from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Question
        read_only_fields = ('status', 'answered_by', 'author_email')
        fields = ( 'status', 'description', 'ask_date', 'author_email')
    def create(self, validated_data):
        question =  models.Question.objects.create(**validated_data)
        question.status = "Not answered"
        user_email = (self.context["user"])
        if len(user_email) != 0:
            question.author_email = user_email
        question.save()
        return question