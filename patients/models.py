from django.db import models
from django.core.validators import RegexValidator


class Patient(models.Model):

    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
        ("N", "Not specified"),
    ]

    # Identification
    full_name = models.CharField(max_length=150)
    birth_date = models.DateField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default="N")
    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[
            RegexValidator(r"^\d{11}$", "CPF must contain exactly 11 digits.")
        ],
        help_text="Optional, but must be unique if provided."
    )

    # Contact
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Basic clinical data
    allergies = models.TextField(null=True, blank=True)
    pre_existing_conditions = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} ({self.birth_date})"

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        ordering = ["full_name"]

class Mammogram(models.Model):
    patient = models.ForeignKey(
        Patient,
        related_name='mammograms',
        on_delete=models.CASCADE
    )
    image = models.ImageField(upload_to='mammograms/', null=True, blank=True)