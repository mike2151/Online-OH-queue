from rest_framework import serializers
from .models import Question
from django.contrib.auth import get_user_model
from ohqueue.models import OHQueue


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        read_only_fields = ('status', 'answered_by', 'author_email')
        fields = ( 'status', 'description', 'ask_date', 'author_email')
    def create(self, validated_data):
        question =  Question.objects.create(**validated_data)
        question.status = "Not answered"
        user_email = (self.context["user"])
        if len(user_email) != 0:
            question.author_email = user_email
        question.save()
        
        name_of_ohqueue = (self.context["queue"])
        if len(name_of_ohqueue) != 0:
            # see if ohqueue exists
            ohqueue = OHQueue.objects.filter(name=name_of_ohqueue).first()
            if ohqueue != None:
                # add the question
                ohqueue.questions.add(question)
                ohqueue.save()
        return question