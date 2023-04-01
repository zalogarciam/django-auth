from rest_framework.serializers import ModelSerializer
from .models import Mascota, Usuario

class RegistroUsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class MascotaSerializer(ModelSerializer):
    class Meta:
        model = Mascota
        fields = '__all__'

    # def to_representation(self, instance):
    #     # print(super().to_representation(instance))
    #     print(instance.foto.url)
    #     representation = super().to_representation(instance)
    #     print('ISTANCE' , instance.foto.url)

    #     representation.foto =  instance.foto.url
    #     return super().to_representation(instance)