from rest_framework import serializers
from .models import Question
from django.contrib.auth import get_user_model
from ohqueue.models import OHQueue

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        read_only_fields = ('is_answered', 'answered_by', 'author_email', 'author_first_name', 'author_last_name', 'answered_by_email')
        fields = ( 'is_answered', 'description', 'ask_date', 'author_email', 'author_first_name', 'author_last_name', 'answered_by_email')
    def create(self, validated_data):
        question =  Question.objects.create(**validated_data)
        question.is_answered = False
        user_email = (self.context["user"])
        user_first_name = (self.context["user-first-name"])
        user_last_name = (self.context["user-last-name"])
        user_email = (self.context["user"])
        if len(user_email) != 0:
            question.author_email = user_email
        if len(user_first_name) != 0:
            question.author_first_name = user_first_name
        if len(user_last_name) != 0:
            question.author_last_name = user_last_name
        question.save()
        
        name_of_ohqueue = (self.context["queue"])
        if len(name_of_ohqueue) != 0:
            # see if ohqueue exists
            ohqueue = OHQueue.objects.filter(name=name_of_ohqueue).first()
            if ohqueue != None:
                # add the question
                ohqueue.questions.add(question)
                ohqueue.save()
        
        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            'ohqueue',
            {
                'type': 'ohqueue.update',
                'message': 'update'
            }
        )

        return question