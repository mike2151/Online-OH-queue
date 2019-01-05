from rest_framework import permissions
from users.models import StudentUser

class TAPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        token_header = request.META.get('HTTP_AUTHORIZATION')
        if token_header == None or " " not in token_header: 
            return False 
        
        actual_token = token_header.split(" ")[1]
        user = StudentUser.objects.filter(auth_token=actual_token).first() 
        if user == None or not user.is_ta:
            return False
        
        return True