from django.views import View
from django.http import JsonResponse
from django.conf import settings
import os

class GetThemeVariablesView(View):
    def get(self, request,  *args, **kwargs):
       primary_theme_color = os.environ.get('PRIMARY_THEME_COLOR', '#445B73')
       course_title = settings.COURSE_TITLE
       oh_url = settings.OFFICE_HOURS_URL
       favicon_url = os.environ.get('FAVICON_URL','https://www.dropbox.com/s/u10bzo5t2ryx1m1/favicon.ico') 
       return JsonResponse({
           "primary_theme_color": primary_theme_color,
           "course_title": course_title,
           "oh_url": oh_url,
           "favicon_url": favicon_url
       })
