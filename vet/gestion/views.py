from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import MascotaSerializer, RegistroUsuarioSerializer
from .models import Mascota, Usuario
from rest_framework.permissions import IsAuthenticated
from .permissions import SoloClientes
from cloudinary import uploader
from rest_framework import generics
from django.forms.models import model_to_dict

class RegistroUsuario(generics.GenericAPIView):
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
    
class PerfilUsuario(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, SoloClientes]
    def get(self, request: Request):
        # TODO: Devolver el usuario, NO DEVOLVER LA PASSWORD solamente el nombre, apellido, correo y tipoUsuario utilizando un serializador
        # serializador = RegistroUsuarioSerializer(data = request.data)
        # print(serializador)

        user = Usuario.objects.filter(correo = request.user).first()

        if not user:
            return Response(
                data = {
                'content': 'Usuario no existe...'
                }, status=status.HTTP_404_NOT_FOUND
            )
        print(type(user))
        serializador = RegistroUsuarioSerializer(user)

        return Response(
                data = {
                'content': {
                    'nombre': serializador.data['nombre'],
                    'apellido': serializador.data['apellido'],
                    'correo': serializador.data['correo'],
                    'tipoUsuario': serializador.data['tipoUsuario']
                }

                }, status=status.HTTP_200_OK
            )
    
class MascotasView(generics.GenericAPIView):
    serializer_class = MascotaSerializer
    permission_classes = [IsAuthenticated, SoloClientes]


    def post(self, request:Request):
        foto = request.FILES.get('foto')
        resultado = uploader.upload(foto)
        try:
          data = {
              'nombre': request.data.get('nombre'),
              'sexo': request.data.get('sexo'),
              'fechaNacimiento': request.data.get('fechaNacimiento'),
              'alergias': request.data.get('alergias'),
              'foto': resultado.get('url'),
              'cliente': request.data.get('cliente')
          }

          print('DATA', data)

          serializador = MascotaSerializer(data=data)
          if serializador.is_valid():
              serializador.save()
              return Response(data= {
                  'message': 'Mascota creada exitosamente',
                  'content': serializador.data
              }, status=status.HTTP_201_CREATED)
          else:
              return Response(data={
                  'message': 'Error al crear mascota',
                  'content': serializador.errors
              }, status=status.HTTP_400_BAD_REQUEST)
          
        except Exception as e:
          return Response(data={
              'message': 'Error al crear mascota',
              'content': str(e)
          }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request):
        mascotas = Mascota.objects.all()
        serializador = MascotaSerializer(mascotas, many = True)
        print(serializador.data)
        return Response(data = {
            'content': serializador.data
        }, status= status.HTTP_200_OK)