from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.conf import settings


from .forms import StudentUserCreationForm, StudentUserChangeForm
from .models import StudentUser

class StudentUserAdmin(UserAdmin):
    add_form = StudentUserCreationForm
    form = StudentUserChangeForm
    model = StudentUser
    list_display = ['email', 'first_name', 'last_name', 'is_ta', 'is_active', 'username']

admin.site.site_header = settings.COURSE_TITLE  + ' Office Hours Admin'
admin.site.register(StudentUser, StudentUserAdmin)
admin.site.unregister(Group)
admin.site.unregister(Site)