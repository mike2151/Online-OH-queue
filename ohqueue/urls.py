from django.urls import include, path

from . import views

urlpatterns = [
    path('create/', views.OHQueueCreationView.as_view()),
    path('<name>/ask', views.QuestionCreationView.as_view(), name='ask'),
]