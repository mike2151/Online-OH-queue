from django.urls import include, path

from . import views

urlpatterns = [
    path('frequentasker/<start>/<end>/', views.FrequentUserView.as_view()),
    path('frequentanswer/<start>/<end>/', views.FrequentAnswerView.as_view()),
    path('all_feedback_data/<start>/<end>/', views.AllFeedbackView.as_view()),
    path('<email>/questions/', views.UserTimeSeriesView.as_view()),
    path('<email>/feedback/<start>/<end>/', views.TAFeedbackView.as_view()),
    path('getstudents/', views.GetAllStudentsView.as_view()),
    path('gettas/', views.GetAllTasView.as_view()),
    path('traffictime/<start>/<end>/', views.GetTrafficTimesView.as_view())
]

