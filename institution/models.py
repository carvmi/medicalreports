from django.db import models

# Create your models here.
class Address(models.Model):
    rua = models.CharField(max_length=120)
    cep = models.CharField(max_length=20)
    bairro = models.CharField(max_length=60)
    cidade = models.CharField(max_length=60)
    uf = models.CharField(max_length=2)

class Institution(models.Model):
    nome = models.CharField(max_length=120)
    endereco_fisico = models.OneToOneField(Address, on_delete=models.CASCADE)
    endereco_eletronico = models.EmailField()
    tipo = models.CharField(max_length=50)
    logo = models.ImageField(upload_to='logos/', null=True, blank=True)
