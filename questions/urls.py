from django.urls import include, path

from . import views

urlpatterns = [
    path('answer/', views.QuestionAnswerView.as_view(), name='answer'),
]