from django.db import models
from patients.models import Patient

class MammogramExam(models.Model):
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="mammograms"
    )

    exam_date = models.DateField()
    description = models.TextField(null=True, blank=True)
    result = models.CharField(
        max_length=50,
        null=True,
        blank=True
    )
    acceptance_term = models.BooleanField(default=False)

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
