# from django.db import models

# class Report(models.Model):
#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     local = models.ForeignKey(Institution, on_delete=models.CASCADE)

#     nome_laudo = models.CharField(max_length=120)
#     data_criacao = models.DateTimeField(auto_now_add=True)
#     ip_usuario = models.GenericIPAddressField()
#     termo_aceitacao = models.BooleanField(default=False)
    
#     # Campo que receberá a resposta da IA
#     resultado_ia = models.JSONField(null=True, blank=True)
# Vincular o logotipo aqui depois de acrescentar em institution 