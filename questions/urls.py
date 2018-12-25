from django.urls import include, path

from . import views

urlpatterns = [
    path('answer/<int:pk>', views.QuestionAnswerView.as_view(), name='answer'),
]