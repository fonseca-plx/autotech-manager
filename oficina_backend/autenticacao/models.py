from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Usuario(AbstractUser):
    PERFIL = (
        ('gerente', 'GERENTE'),
        ('mecanico', 'MECANICO'),
        ('cliente', 'CLIENTE'),
    )
    username = None
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=11, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    tipo_perfil = models.CharField(max_length=10, choices=PERFIL)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    ativo = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['cpf', 'tipo_perfil']

    def __str__(self):
        return f"{self.email} - {self.tipo_perfil}"