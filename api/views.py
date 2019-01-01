from django.views import View
from django.http import JsonResponse
import os

class GetThemeVariablesView(View):
    def get(self, request,  *args, **kwargs):
       primary_theme_color = os.environ.get('PRIMARY_THEME_COLOR', '#76b852')
       return JsonResponse({"primary_theme_color": primary_theme_color})