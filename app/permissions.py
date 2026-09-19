from rest_framework.permissions import BasePermission

class HasProfile(BasePermission):
    message="You must have a profile to continue"
    def has_permission(self, request, view):
        try:
            profile=request.user.user_profile
            if profile:
                return True
            else:
                return False
        except Exception as e:
            return False