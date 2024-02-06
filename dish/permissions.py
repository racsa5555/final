from rest_framework.permissions import BasePermission
from rest_framework.permissions import AllowAny

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
    
