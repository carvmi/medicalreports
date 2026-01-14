from django.db import models

class Address(models.Model):
 rua = models.CharField(max_length=120)
 cep = models.CharField(max_length=20)
 bairro = models.CharField(max_length=60)
 cidade = models.CharField(max_length=60)
 uf = models.CharField(max_length=2)
 number = models.CharField(max_length=5, default = '0')
 def __str__ (self):
    return f'{self.bairro} - {self.cidade} - {self.uf} - {self.number} '

class TypesInstitution(models.TextChoices):
    CLINICA = 'C', ('Clinica')
    HOSPITAL = 'H', ('Hospital')
    UNID_MOVEL = 'UM', ('Unidade Móvel')

class Institution(models.Model):
    name = models.CharField(max_length=120)
    endereco_fisico = models.OneToOneField(Address, on_delete=models.CASCADE, null = True)
    site = models.CharField(max_length=120, blank = True)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=120)
    itype = models.CharField(
        max_length=2,
        choices = TypesInstitution.choices,
        default = TypesInstitution.HOSPITAL)
    def __str__(self):
        return f'{self.itype} - {self.name}'
    logo = models.ImageField(upload_to='institution/media', null=True, blank=True)
