from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('answer/', csrf_exempt(views.QuestionAnswerView.as_view()), name='answer'),
    path('delete/', csrf_exempt(views.QuestionDeleteView.as_view()), name='delete'),
    path('detail/<questionid>/', views.QuestionInformation.as_view(), name="detail"),
]