from django.db import models
from patients.models import Patient
from institution.models import Institution
    
class Status(models.TextChoices):
        PENDENTE = "PENDENTE", "Pendente"
        PRONTO = "PRONTO", "Laudo Pronto" 
        ENTREGUE = "ENTREGUE", "Laudo Entregue"
        CANCELADO = "CANCELADO", "Laudo Cancelado"

class Result(models.TextChoices):
        SAUDAVEL = "SAUDAVEL", "Saudavel"
        BENIGNO = "BENIGNO", "Benigno"
        MALIGNO = "MALIGNO", "Maligno"
        INDETERMINADO = "INDETERMINADO", "Indeterminado"


class MammogramExam(models.Model):

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="mammograms"
    )

    local = models.ForeignKey(Institution, on_delete=models.CASCADE, null = True)
    exam_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    result = models.CharField(
        max_length=50,
        choices = Result.choices,
        default = Result.SAUDAVEL)

    itype = models.CharField(
        max_length=9,
        choices = Status.choices,
        default = Status.PENDENTE)
    acceptance_term = models.BooleanField(default=False)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="mammograms/", null=True, blank=True)

    def __str__(self):
        return f"Exame - {self.patient.full_name} {self.exam_date} {self.itype}"