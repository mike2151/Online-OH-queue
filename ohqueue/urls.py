from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path('list/', views.OHQueueListView.as_view()),
    path('list_ta/', views.OHQueueTAListView.as_view()),
    path('<name>/ask', views.QuestionCreationView.as_view(), name='ask'),
    path('question/<questionid>/edit', views.QuestionEditView.as_view(), name='edit'),
    path('open/', csrf_exempt(views.OpenQueueExtended.as_view()), name='open'),
    path('close/', csrf_exempt(views.CloseQueue.as_view()), name='close'),
]