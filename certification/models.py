from django.db import models
from citizen.models import Citizen


class Certification(models.Model):
    CERTIFICATE_TYPE_CHOICES = [
        ('birth', 'Birth Certificate'),
        ('death', 'Death Certificate'),
        ('marriage', 'Marriage Certificate'),
        ('character', 'Character Certificate'),
        ('income', 'Income Certificate'),
        ('residence', 'Residence Certificate'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='certifications')
    certificate_type = models.CharField(max_length=50, choices=CERTIFICATE_TYPE_CHOICES)
    certificate_number = models.CharField(max_length=50, unique=True)
    issue_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Certification"
        verbose_name_plural = "Certifications"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_certificate_type_display()} - {self.citizen}"
