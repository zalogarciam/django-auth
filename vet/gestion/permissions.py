from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from .models import Usuario

class SoloClientes(BasePermission):
    message = "Solo los clientes pueden realizar esta peticion"
    def has_permission(self, request:Request, view):
        usuario: Usuario = request.user

        if usuario.tipoUsuario == 'CLIENTE':
            return True
        else:
            return False