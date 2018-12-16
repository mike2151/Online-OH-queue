from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists

class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_username(self, username):
        username = get_adapter().clean_username(username)
        return username

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered with this e-mail address."))
        if "upenn.edu" not in email:
            raise serializers.ValidationError("Email is not a Penn Email")
        return email

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        return data

    class Meta:
        model = models.StudentUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def get_cleaned_data(self):
        return {
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'email': self.validated_data.get('email', '')
        }
    def custom_signup(self, request, user):
        pass

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user