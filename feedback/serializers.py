from rest_framework import serializers
from .models import Feedback
from channels.layers import get_channel_layer
from users.models import StudentUser


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        read_only_fields = ('ta_email', 'base_question', 'feedback_time',)
        fields = ( 'helpful_scale', 'was_helpful', 'comments', 'feedback_time', 'ta_email', 'base_question', )
    def create(self, validated_data):
        user_email = (self.context["user"])

        if len(user_email) == 0:
            raise serializers.ValidationError('Error: User is not valid')

        feedback = Feedback.objects.create(**validated_data)
        
        user = StudentUser.objects.filter(email=user_email).first()
        question = user.most_recent_question

        feedback.ta_email = question.answered_by_email
        feedback.base_question = question
        feedback.save()

        question.feedback_for_q = feedback
        question.save()
        
        return feedback
    