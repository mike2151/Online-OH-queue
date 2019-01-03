from django.urls import include, path

from . import views

urlpatterns = [
    path('list/', views.OHQueueListView.as_view()),
    path('list_ta/', views.OHQueueTAListView.as_view()),
    path('<name>/ask', views.QuestionCreationView.as_view(), name='ask'),
    path('open/', views.OpenQueueExtended.as_view(), name='open'),
    path('close/', views.CloseQueue.as_view(), name='close'),
]