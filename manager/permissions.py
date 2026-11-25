from rest_framework.permissions import BasePermission


class TemPerfil(BasePermission):
    def has_permission(self, request, view):
   
        return request.user.is_authenticated and hasattr(request.user, 'perfil')