from django.db import models
from patients.models import Patient
from institution.models import Institution
    
class Status(models.TextChoices):
        PENDING = "PENDING", "Pendente"
        READY = "READY", "Laudo Pronto" 
        DELIVERED = "DELIVERED", "Laudo Entregue"
        CANCELED = "CANCELED", "Laudo Cancelado"

class Result(models.TextChoices):
        SAUDAVEL = "SAUDAVEL", "Saudavel"
        BENIGN = "BENIGN", "Benigno"
        MALIGNANT = "MALIGNANT", "Maligno"
        INDETERMINATE = "INDETERMINATE", "Indeterminado"


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
        default = Status.PENDING)
    acceptance_term = models.BooleanField(default=False)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Exame - {self.patient.full_name} {self.exam_date} {self.itype}"

class MammogramImage(models.Model):
    exam = models.ForeignKey(
        MammogramExam,
        on_delete=models.CASCADE,
        related_name="images"
    )

    image = models.ImageField(upload_to="mammograms/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for exam {self.exam.id}"
