from django.db import models
from citizen.models import Citizen


class TradeLicense(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('expired', 'Expired'),
    ]

    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='trade_licenses')
    license_number = models.CharField(max_length=50, unique=True)
    business_name = models.CharField(max_length=200)
    business_type = models.CharField(max_length=100)
    business_address = models.TextField()
    issue_date = models.DateField()
    expiry_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    license_fee = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trade License"
        verbose_name_plural = "Trade Licenses"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.business_name} - {self.license_number}"
