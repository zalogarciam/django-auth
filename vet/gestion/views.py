from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegistroUsuarioSerializer
from .models import Usuario
from rest_framework.permissions import IsAuthenticated
from .permissions import SoloClientes
from cloudinary import uploader
class RegistroUsuario(APIView):
    def post(self, request: Request): 
        serializador = RegistroUsuarioSerializer(data = request.data)
        if serializador.is_valid():
            password = serializador.validated_data.get('password')

            nuevo_usuario = Usuario(**serializador.validated_data)
            
            nuevo_usuario.set_password(password)
            nuevo_usuario.save()

            return Response(
                data = {
                'message': 'Usuario creado'
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                data = {
                'message': 'Error crear usuario',
                'content': serializador.errors
                }, status=status.HTTP_400_BAD_REQUEST
            )
    
class PerfilUsuario(APIView):
    permission_classes = [IsAuthenticated, SoloClientes]
    def get(self, request: Request):
        
        print(request.user)
        print(request.auth)
        return Response(
            data = {
            'content': ''
            }
        )
    
class Mascotas(APIView):
    permission_classes = [IsAuthenticated, SoloClientes]
    def post(self, request:Request):
        foto = request.FILES.get('foto')
        print(foto)
        result = uploader.upload(file = foto)
        if result:
            return Response(data = {
                'message': 'Mascota creada'

            }, status=status.HTTP_201_CREATED)
        else:
            return Response(data = {
                'message': 'Error'
            })