from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from citizen.models import Citizen


class Area(models.Model):
    """Area/Ward classification."""

    name = models.CharField(_("Area Name"), max_length=100)
    code = models.CharField(_("Area Code"), max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class Street(models.Model):
    """Street/Road classification."""

    name = models.CharField(_("Street Name"), max_length=200)
    code = models.CharField(_("Street Code"), max_length=20, unique=True, blank=True, null=True)
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="streets"
    )
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Street")
        verbose_name_plural = _("Streets")
        ordering = ["area", "name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["area"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.area.name}"


class PropertyType(models.Model):
    """Property type classification."""

    name = models.CharField(_("Property Type Name"), max_length=100, unique=True)
    code = models.CharField(_("Property Type Code"), max_length=20, unique=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Property Type")
        verbose_name_plural = _("Property Types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Property(models.Model):
    """Holding/Property information."""

    STATUS_CHOICES = [
        ("DRAFT", _("Draft")),
        ("PENDING_APPROVAL", _("Pending Approval")),
        ("APPROVED", _("Approved")),
        ("REJECTED", _("Rejected")),
    ]

    property_number = models.CharField(
        _("Holding Number"), max_length=50, unique=True
    )
    property_type = models.ForeignKey(
        PropertyType, on_delete=models.PROTECT, related_name="properties"
    )
    owner = models.ForeignKey(
        Citizen, on_delete=models.PROTECT, related_name="properties"
    )
    address = models.TextField(_("Property Address"), help_text=_("Detailed address (house number, building name, etc.)"))
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name="properties", blank=True, null=True
    )
    street = models.ForeignKey(
        Street, on_delete=models.PROTECT, related_name="properties", blank=True, null=True
    )
    city = models.CharField(_("City"), max_length=100, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)
    area_sqft = models.DecimalField(
        _("Area (sq ft)"),
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        help_text=_("Total area in square feet"),
    )
    assessed_value = models.DecimalField(
        _("Assessed Value"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text=_("Assessed property value"),
    )
    tax_rate = models.DecimalField(
        _("Tax Rate (%)"),
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
        help_text=_("Tax rate as percentage"),
    )
    is_active = models.BooleanField(_("Is Active"), default=True)
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="DRAFT",
        help_text=_("Workflow status of the holding"),
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="properties_created",
    )
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties_submitted",
        verbose_name=_("Submitted By"),
    )
    submitted_at = models.DateTimeField(
        _("Submitted At"), null=True, blank=True, help_text=_("When the holding was submitted for approval")
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="properties_approved",
        verbose_name=_("Approved By"),
    )
    approved_at = models.DateTimeField(
        _("Approved At"), null=True, blank=True, help_text=_("When the holding was approved")
    )
    rejection_reason = models.TextField(
        _("Rejection Reason"), blank=True, help_text=_("Reason for rejection if applicable")
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Holding")
        verbose_name_plural = _("Holdings")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["property_number"]),
            models.Index(fields=["owner"]),
            models.Index(fields=["city"]),
            models.Index(fields=["area"]),
            models.Index(fields=["street"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.property_number} - {self.owner.full_name}"

    @property
    def annual_tax_amount(self):
        """Calculate annual tax amount."""
        if self.assessed_value and self.tax_rate:
            return (self.assessed_value * self.tax_rate) / Decimal("100.00")
        return Decimal("0.00")

    def can_edit(self, user):
        """Check if user can edit this holding."""
        if self.status != "DRAFT":
            return False
        if self.created_by != user:
            return False
        return True

    def can_submit(self, user):
        """Check if user can submit this holding."""
        if self.status != "DRAFT":
            return False
        if self.created_by != user:
            return False
        return True

    def can_approve(self, user):
        """Check if user can approve this holding."""
        if self.status != "PENDING_APPROVAL":
            return False
        return user.groups.filter(name="Officer").exists()


class TaxPeriod(models.Model):
    """Tax period (e.g., Financial Year)."""

    name = models.CharField(_("Period Name"), max_length=100)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"))
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tax Period")
        verbose_name_plural = _("Tax Periods")
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"


class HoldingTax(models.Model):
    """Holding tax assessment and payment record."""

    STATUS_CHOICES = [
        ("PENDING", _("Pending")),
        ("PAID", _("Paid")),
        ("PARTIAL", _("Partially Paid")),
        ("OVERDUE", _("Overdue")),
        ("WAIVED", _("Waived")),
    ]

    tax_number = models.CharField(_("Tax Number"), max_length=50, unique=True)
    holding_property = models.ForeignKey(
        Property, on_delete=models.PROTECT, related_name="holding_taxes"
    )
    tax_period = models.ForeignKey(
        TaxPeriod, on_delete=models.PROTECT, related_name="holding_taxes"
    )
    tax_amount = models.DecimalField(
        _("Tax Amount"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    paid_amount = models.DecimalField(
        _("Paid Amount"),
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    due_date = models.DateField(_("Due Date"))
    status = models.CharField(
        _("Status"), max_length=20, choices=STATUS_CHOICES, default="PENDING"
    )
    penalty_amount = models.DecimalField(
        _("Penalty Amount"),
        max_digits=15,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[MinValueValidator(Decimal("0.00"))],
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="holding_taxes_created",
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Holding Tax")
        verbose_name_plural = _("Holding Taxes")
        ordering = ["-due_date", "-created_at"]
        indexes = [
            models.Index(fields=["tax_number"]),
            models.Index(fields=["holding_property"]),
            models.Index(fields=["status"]),
            models.Index(fields=["due_date"]),
        ]

    def __str__(self):
        return f"{self.tax_number} - {self.holding_property.property_number} - {self.tax_amount}"

    @property
    def balance_amount(self):
        """Calculate remaining balance."""
        tax = self.tax_amount or Decimal("0.00")
        penalty = self.penalty_amount or Decimal("0.00")
        paid = self.paid_amount or Decimal("0.00")
        return tax + penalty - paid

    def is_overdue_check(self):
        """Check if tax is overdue."""
        from django.utils import timezone
        return self.due_date < timezone.now().date() and self.status != "PAID"


class AttachmentType(models.Model):
    """Attachment type classification for property documents."""

    name = models.CharField(_("Attachment Type Name"), max_length=100, unique=True)
    code = models.CharField(_("Attachment Type Code"), max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    is_active = models.BooleanField(_("Is Active"), default=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Attachment Type")
        verbose_name_plural = _("Attachment Types")
        ordering = ["name"]

    def __str__(self):
        return self.name


class PropertyAttachment(models.Model):
    """Property attachment/document model."""

    property = models.ForeignKey(
        Property, on_delete=models.CASCADE, related_name="attachments"
    )
    attachment_type = models.ForeignKey(
        AttachmentType, on_delete=models.PROTECT, related_name="attachments"
    )
    title = models.CharField(_("Title"), max_length=200)
    description = models.TextField(_("Description"), blank=True)
    file = models.FileField(
        _("File"), upload_to="property_attachments/%Y/%m/%d/"
    )
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="property_attachments_uploaded",
    )
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Property Attachment")
        verbose_name_plural = _("Property Attachments")
        ordering = ["-uploaded_at"]
        indexes = [
            models.Index(fields=["property"]),
            models.Index(fields=["attachment_type"]),
            models.Index(fields=["uploaded_at"]),
        ]

    def __str__(self):
        return f"{self.property.property_number} - {self.title} ({self.attachment_type.name})"


class TaxPayment(models.Model):
    """Tax payment record."""

    PAYMENT_METHOD_CHOICES = [
        ("CASH", _("Cash")),
        ("CHEQUE", _("Cheque")),
        ("BANK_TRANSFER", _("Bank Transfer")),
        ("ONLINE", _("Online Payment")),
        ("OTHER", _("Other")),
    ]

    payment_number = models.CharField(
        _("Payment Number"), max_length=50, unique=True
    )
    holding_tax = models.ForeignKey(
        HoldingTax, on_delete=models.PROTECT, related_name="payments"
    )
    payment_date = models.DateField(_("Payment Date"))
    amount = models.DecimalField(
        _("Amount"),
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
    )
    payment_method = models.CharField(
        _("Payment Method"), max_length=20, choices=PAYMENT_METHOD_CHOICES
    )
    reference_number = models.CharField(_("Reference Number"), max_length=100, blank=True)
    cheque_number = models.CharField(_("Cheque Number"), max_length=50, blank=True)
    bank_name = models.CharField(_("Bank Name"), max_length=100, blank=True)
    notes = models.TextField(_("Notes"), blank=True)
    received_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tax_payments_received",
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Tax Payment")
        verbose_name_plural = _("Tax Payments")
        ordering = ["-payment_date", "-created_at"]
        indexes = [
            models.Index(fields=["payment_date"]),
            models.Index(fields=["holding_tax"]),
        ]

    def __str__(self):
        return f"{self.payment_number} - {self.holding_tax.tax_number} - {self.amount}"
