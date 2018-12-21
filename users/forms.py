from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import StudentUser

class StudentUserCreationForm(UserCreationForm):

    def clean_email(self):
        data = self.cleaned_data['email']
        if "upenn.edu" not in data:
            raise forms.ValidationError("Email is not a Penn Email")
        return data   

    class Meta(UserCreationForm):
        model = StudentUser
        fields = ('username', 'email', 'first_name', 'last_name') 

class StudentUserChangeForm(UserChangeForm):

    class Meta:
        model = StudentUser
        fields = UserChangeForm.Meta.fields