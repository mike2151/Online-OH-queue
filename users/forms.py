from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import StudentUser

class StudentUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = StudentUser
        fields = ('username', 'email', 'first_name', 'last_name')

class StudentUserChangeForm(UserChangeForm):

    class Meta:
        model = StudentUser
        fields = UserChangeForm.Meta.fields