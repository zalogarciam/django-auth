from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin

class ManejoUsuario(BaseUserManger):
    def create_superuser(self, correo, nombre, apellido, password, tipoUsuario)
        if not correo:
            raise ValueError('El usuario debe tener un correo')
        
        correo_normalizado = self.normalize_email(correo)
        nuevo_usuario = self.model(correo = correo_normalizado, nombre = nombre, apellido = apellido, tipoUsuario = tipoUsuario)

        nuevo_usuario.set_password(password)

        nuevo_usuario.is_superuser = True
        nuevo_usuario.is_staff =  True

        nuevo_usuario.save()

class Usuario(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)

    nombre = models.TextField(null =False)
    apellido = models.TextField(null=False)
    correo = models.EmailField(max_length=100, unique =True, null=False)
    password = models.TextField(null =False)

    tipoUsuario = models.CharField(max_length=100, chices = [('ADMIN', 'ADMIN'), ('CLIENTE', 'CLIENTE')])
    db_column = 'tipo_usuario'

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'correo'

    REQUIRE_FIELDS = ['nombre', 'apellido']

    class Meta:
        db_table = 'usuarios'