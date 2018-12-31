from django.shortcuts import render

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django.views import View
from .models import OHQueue
from questions.models import Question
from .serializers import OHQueueSerializer
from questions.serializers import QuestionSerializer
from rest_framework.response import Response
from users.models import StudentUser
from django.http import JsonResponse
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


class OHQueueCreationView(generics.CreateAPIView):
    queryset = OHQueue.objects.all()
    serializer_class = OHQueueSerializer
    permission_classes = (IsAdminUser,)

class OHQueueListView(generics.ListAPIView):
    queryset = OHQueue.objects.all()
    serializer_class = OHQueueSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
       all_queues = OHQueue.objects.all()
       active_queues_id = [o.id for o in all_queues if o.isQueueActive()]
       queues = all_queues.filter(id__in=active_queues_id)
       return queues

class OHQueueTAListView(generics.ListAPIView):
    queryset = OHQueue.objects.all()
    serializer_class = OHQueueSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None or not user.is_ta:
           return OHQueue.objects.none()

       all_queues = OHQueue.objects.all()
       active_queues_id = [o.id for o in all_queues if o.updateTime()]
       queues = all_queues.filter(id__in=active_queues_id)
       return queues

class QuestionCreationView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAuthenticated,)

    def get_serializer_context(self):
        ohqueuename = (self.kwargs["name"])
        token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
        if token_header == None:
            return JsonResponse({"error": "No authentication found"})
        # seperate token from Token xyz
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first()
        return {'user': user.email, 'user-first-name': user.first_name, 'user-last-name': user.last_name, 'queue': ohqueuename}

class OpenQueueExtended(View):
    def post(self, request,  *args, **kwargs):
       # get current TA
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None or not user.is_ta:
           return JsonResponse({"success": False, "error": "You are not authenticated"})

       # get queue
       queue_name = (json.loads(request.body.decode())["queue"])
       queue = None
       try:
            queue = OHQueue.objects.get(name=queue_name)
       except:
            queue = None
       if queue == None:
            return JsonResponse({"success": False, "error": "Queue does not exist"})
       if queue.is_open_extended:
           queue.is_open_extended = False
       else:
           queue.is_open_extended = True
           queue.is_closed = False
       queue.save()

       layer = get_channel_layer()
       async_to_sync(layer.group_send)(
            'ohqueue',
            {
                'type': 'ohqueue.update',
                'message': 'update'
            }
        )

       return JsonResponse({"success": True})

class CloseQueue(View):
    def post(self, request,  *args, **kwargs):
       # get current TA
       token_header = (self.request.META.get('HTTP_AUTHORIZATION'))
       actual_token = token_header.split(" ")[1]
       user = StudentUser.objects.filter(auth_token=actual_token).first()
       if user == None or not user.is_ta:
           return JsonResponse({"success": False, "error": "You are not authenticated"})

       # get queue
       queue_name = (json.loads(request.body.decode())["queue"])
       queue = None
       try:
            queue = OHQueue.objects.get(name=queue_name)
       except:
            queue = None
       if queue == None:
            return JsonResponse({"success": False, "error": "Queue does not exist"})
       if queue.is_closed:
          queue.is_closed = False
       else:
          queue.is_closed = True
          queue.is_open_extended = False
       queue.save()

       layer = get_channel_layer()
       async_to_sync(layer.group_send)(
            'ohqueue',
            {
                'type': 'ohqueue.update',
                'message': 'update'
            }
        )

       return JsonResponse({"success": True})