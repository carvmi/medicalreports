from django.db import models

# # # =Create your models here.
#class Address(models.Model):
 #rua = models.CharField(max_length=120)
 #cep = models.CharField(max_length=20)
 #bairro = models.CharField(max_length=60)
 #cidade = models.CharField(max_length=60)
 #uf = models.CharField(max_length=2)

class TypesInstitution(models.TextChoices):
    CLINICA = 'C', ('Clinica')
    HOSPITAL = 'H', ('Hospital')
    UNID_MOVEL = 'UM', ('Unidade Móvel')

class Institution(models.Model):
    name = models.CharField(max_length=120)
    #endereco_fisico = models.OneToOneField(Address, on_delete=models.CASCADE)
    site = models.CharField(max_length=120)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=120)
    itype = models.CharField(
        max_length=2,
        choices = TypesInstitution.choices,
        default = TypesInstitution.HOSPITAL)
    #logo = models.ImageField(upload_to='logos/', null=True, blank=True)
