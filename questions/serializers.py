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

        user_first_name = (self.context["user-first-name"])
        user_last_name = (self.context["user-last-name"])
        user_email = (self.context["user"])

        if len(user_email) == 0 or len(user_first_name) == 0 or len(user_last_name) == 0:
            raise serializers.ValidationError('Error: User is not valid')

        name_of_ohqueue = (self.context["queue"])
        ohqueue = None
        if len(name_of_ohqueue) != 0:
            # see if ohqueue exists
            ohqueue = OHQueue.objects.filter(name=name_of_ohqueue).first()
            if ohqueue == None:
                raise serializers.ValidationError('Error: Invalid Queue')
        else:
            raise serializers.ValidationError('Error: Invalid Queue')

        # make sure the student has not asked any other question
        userInQueues = False
        all_queues = OHQueue.objects.all()
        for queue in all_queues:
            for question in queue.questions.all():
                if question.author_email == user_email:
                    userInQueues = True
                    break
        if userInQueues:
            raise serializers.ValidationError('Error: You already asked a question')

        question = Question.objects.create(**validated_data)
        question.is_answered = False
        
        question.author_email = user_email
        question.author_first_name = user_first_name
        question.author_last_name = user_last_name
        question.save()

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
    