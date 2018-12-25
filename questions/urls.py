from django.urls import include, path

from . import views

urlpatterns = [
    path('<queue>/answer/<int:pk>', views.QuestionAnswerView.as_view(), name='answer'),
]