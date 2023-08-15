from rest_framework.permissions import BasePermission, SAFE_METHODS

class LibrarianAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission to allow read access (GET) to unauthenticated users
    and require authentication for other methods.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True  
        return request.user and request.user.is_authenticated and (request.user.role == 'A' or request.user.role == 'L')

class IsLibrarianAuthenticated(BasePermission):
    """Custom permission to allow only admin or librarian for CRUD."""

    def has_permission(self, request, view): 
        return request.user and request.user.is_authenticated and (request.user.role == 'A' or request.user.role == 'L')

class IsAdminAuthenticated(BasePermission):
    """Custom permission to allow only admin for CRUD."""
    def has_permission(self, request, view): 
        return request.user and request.user.is_authenticated and request.user.role == 'A'

