from django.db import models
from citizen.models import Citizen


class HoldingTax(models.Model):
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    citizen = models.ForeignKey(Citizen, on_delete=models.CASCADE, related_name='holding_taxes')
    holding_number = models.CharField(max_length=50, unique=True)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Holding Tax"
        verbose_name_plural = "Holding Taxes"
        ordering = ['-created_at']

    def __str__(self):
        return f"Holding {self.holding_number} - {self.citizen}"
