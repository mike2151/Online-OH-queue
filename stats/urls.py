from django.urls import include, path

from . import views

urlpatterns = [
    path('frequentasker/', views.FrequentUserView.as_view()),
    path('frequentanswer/', views.FrequentAnswerView.as_view())
]