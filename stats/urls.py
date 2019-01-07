from django.urls import include, path

from . import views

urlpatterns = [
    path('frequentasker/', views.FrequentUserView.as_view()),
    path('frequentanswer/', views.FrequentAnswerView.as_view()),
    path('<email>/questions/', views.UserQuestionsView.as_view()),
    path('getstudents/', views.GetAllStudentsView.as_view()),
    path('traffictime/', views.GetTrafficTimesView.as_view())
]