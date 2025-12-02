from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class Roles(models.TextChoices):
    ADMIN = "ADMIN", "Administrador"
    TECNICO = "TECNICO", "Técnico"
    AUDITOR = "AUDITOR", "Auditor"
    MEDICO = "MEDICO", "Médico"
    BIOMEDICO = "BIOMEDICO", "Biomédico"

class User(AbstractUser):
    cargo = models.CharField(max_length=50, blank=True)
    registro_profissional = models.CharField(max_length=50, blank=True, null=True)

    
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.TECNICO
    )
