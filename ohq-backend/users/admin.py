from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import StudentUserCreationForm, StudentUserChangeForm
from .models import StudentUser

class StudentUserAdmin(UserAdmin):
    add_form = StudentUserCreationForm
    form = StudentUserChangeForm
    model = StudentUser
    list_display = ['email', 'first_name', 'last_name', 'is_ta', 'is_active', 'username']

admin.site.register(StudentUser, StudentUserAdmin)