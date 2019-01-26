from rest_framework import permissions
from users.models import StudentUser

class TAPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user == None or not user.is_ta:
            return False
        
        return True