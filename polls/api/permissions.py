from rest_framework import permissions
from polls.models import User

class IsSuperAdminAuthenticated(permissions.BasePermission):
    """
    Custom permission to only allow access to logged-in super admin users.
    """
    
    def has_permission(self, request, view):
        # Check if user is logged in via session
        user_id = request.session.get('user_id')
        if not user_id:
            return False
        
        try:
            user = User.objects.get(id=user_id)
            return user.super_user
        except User.DoesNotExist:
            return False