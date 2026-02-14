from django.db import models
from apps.institution import models as institutionmodel

class HealthProfessional(models.Model):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    institution = models.ManyToManyField(
        institutionmodel.Institution,
        related_name="professionals"
    )
    specialization = models.CharField(max_length=120)
    professional_registration = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.full_name
