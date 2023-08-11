from rest_framework.permissions import BasePermission, SAFE_METHODS

class AdminAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to allow read access (GET) to unauthenticated users
    and require authentication for other methods.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  
        return request.user and request.user.is_authenticated and (request.user.role == 'A' or request.user.role == 'L')
