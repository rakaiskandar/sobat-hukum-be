from rest_framework.permissions import BasePermission

class IsAdminPermission(BasePermission):
    """
    Custom permission untuk memastikan hanya pengguna dengan role admin yang dapat mengakses.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'