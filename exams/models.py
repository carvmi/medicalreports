from django.db import models
from patients.models import Patient
from institution.models import Institution
    

class MammogramExam(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="mammograms"
    )

    local = models.ForeignKey(Institution, on_delete=models.CASCADE, default=1)
    exam_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    result = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    acceptance_term = models.BooleanField(default=False)
    user_ip = models.GenericIPAddressField(default='127.0.0.1')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mammogram - {self.patient.full_name} ({self.exam_date})"

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
