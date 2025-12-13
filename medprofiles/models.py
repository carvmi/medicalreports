from django.db import models


class Institution(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class HealthProfessional(models.Model):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name="professionals"
    )
    specialization = models.CharField(max_length=120)
    professional_registration = models.CharField(max_length=50)

    def __str__(self):
        return self.full_name
