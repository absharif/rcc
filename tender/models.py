from django.db import models


class Tender(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed'),
        ('awarded', 'Awarded'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    tender_number = models.CharField(max_length=50, unique=True)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    estimated_value = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    document_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tender"
        verbose_name_plural = "Tenders"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.tender_number}"
