
from rest_framework import permissions


class IsReviewAuthorReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow the author of a review to edit or delete it.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_authenticated)
    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.user.is_staff:
            return True
        
        return obj.user == request.user

