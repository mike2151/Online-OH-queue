from django.urls import include, path

from . import views

urlpatterns = [
    path('answer/', views.QuestionAnswerView.as_view(), name='answer'),
    path('delete/', views.QuestionDeleteView.as_view(), name='delete'),
    path('detail/<questionid>', views.QuestionInformation.as_view(), name="detail"),
]