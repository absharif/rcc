from django.db import models


class CitizenCharter(models.Model):
    SERVICE_CHOICES = [
        ('tax', 'Tax Services'),
        ('license', 'License Services'),
        ('certificate', 'Certificate Services'),
        ('complaint', 'Complaint Services'),
        ('other', 'Other Services'),
    ]

    title = models.CharField(max_length=200)
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    description = models.TextField()
    processing_time = models.CharField(max_length=100, help_text="e.g., 7-10 working days")
    required_documents = models.TextField(help_text="List of required documents")
    fees = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Citizen Charter"
        verbose_name_plural = "Citizen Charters"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"
