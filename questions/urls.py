from django.urls import include, path

from . import views

urlpatterns = [
    path('ask/', views.QuestionCreationView.as_view()),
]