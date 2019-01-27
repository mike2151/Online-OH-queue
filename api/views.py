from django.views import View
from django.http import JsonResponse
import os

class GetThemeVariablesView(View):
    def get(self, request,  *args, **kwargs):
       primary_theme_color = os.environ.get('PRIMARY_THEME_COLOR', '#445B73')
       course_title = os.environ.get('COURSE_TITLE','CIS 121') 
       oh_url = os.environ.get('OFFICE_HOURS_URL', 'https://www.cis.upenn.edu/~cis121/current/schedule.html')
       favicon_url = os.environ.get('FAVICON_URL','https://www.dropbox.com/s/u10bzo5t2ryx1m1/favicon.ico') 
       return JsonResponse({
           "primary_theme_color": primary_theme_color,
           "course_title": course_title,
           "oh_url": oh_url,
           "favicon_url": favicon_url
       })
