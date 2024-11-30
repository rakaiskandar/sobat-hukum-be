from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET']:  # Semua orang bisa membaca data
            return True
        return request.user.is_authenticated and request.user.role == 'admin'  # Akses penuh hanya untuk admin
