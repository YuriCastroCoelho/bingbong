from rest_framework.permissions import BasePermission


class TemPerfil(BasePermission):
    def has_permission(self, request, view):
        # hasattr é False se o usuário não tem Perfil (ex.: superusuário sem perfil)
        return request.user.is_authenticated and hasattr(request.user, 'perfil')