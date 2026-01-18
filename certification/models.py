from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from citizen.models import Citizen


class CertificationType(models.Model):
    """Different types of certifications available."""
    
    name = models.CharField(_("Certification Type Name"), max_length=100, unique=True)
    code = models.CharField(_("Certification Type Code"), max_length=50, unique=True)
    description = models.TextField(_("Description"), blank=True)
    fee = models.DecimalField(_("Fee"), max_digits=10, decimal_places=2, default=0.00)
    validity_days = models.IntegerField(_("Validity (Days)"), default=365, help_text=_("Number of days the certificate is valid"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    
    class Meta:
        verbose_name = _("Certification Type")
        verbose_name_plural = _("Certification Types")
        ordering = ["name"]
    
    def __str__(self):
        return self.name


class Certification(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    citizen = models.ForeignKey(Citizen, on_delete=models.PROTECT, related_name='certifications')
    certification_type = models.ForeignKey(CertificationType, on_delete=models.PROTECT, related_name='certifications')
    certificate_number = models.CharField(_("Certificate Number"), max_length=50, unique=True)
    issue_date = models.DateField(_("Issue Date"), null=True, blank=True)
    expiry_date = models.DateField(_("Expiry Date"), null=True, blank=True)
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(_("Remarks"), blank=True)
    rejection_reason = models.TextField(_("Rejection Reason"), blank=True)
    pdf_file = models.FileField(_("PDF Certificate"), upload_to='certificates/%Y/%m/%d/', blank=True, null=True)
    issued_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='certifications_issued', verbose_name=_("Issued By"))
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='certifications_created', verbose_name=_("Created By"))
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Certification")
        verbose_name_plural = _("Certifications")
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['certificate_number']),
            models.Index(fields=['citizen']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.certification_type.name} - {self.citizen.full_name} ({self.certificate_number})"
    
    def is_expired(self):
        """Check if certificate is expired."""
        from django.utils import timezone
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False
    
    def is_valid(self):
        """Check if certificate is valid (approved and not expired)."""
        return self.status == 'approved' and not self.is_expired()
