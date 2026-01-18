from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings


class Citizen(models.Model):
    """Citizen model for managing citizen records."""

    GENDER_CHOICES = [
        ("M", _("Male")),
        ("F", _("Female")),
        ("O", _("Other")),
    ]

    MARITAL_STATUS_CHOICES = [
        ("S", _("Single")),
        ("M", _("Married")),
        ("D", _("Divorced")),
        ("W", _("Widowed")),
    ]

    # Personal Information
    citizen_id = models.CharField(
        _("Citizen ID"),
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text=_("Citizen identification number"),
    )
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    middle_name = models.CharField(_("Middle Name"), max_length=100, blank=True)
    co_name = models.CharField(_("Father / Husband / Company Name"), max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    gender = models.CharField(_("Gender"), max_length=1, choices=GENDER_CHOICES, default="M")
    marital_status = models.CharField(
        _("Marital Status"), max_length=1, choices=MARITAL_STATUS_CHOICES, default="S"
    )
    national_id = models.CharField(
        _("National ID"),
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        help_text=_("National identification number"),
    )

    # Contact Information
    phone_regex = RegexValidator(
        regex=r"^\+?8801?\d{10}$",
        message=_("Phone number must be entered in the format: '+8801XXXXXXXXXX'. Up to 10 digits allowed."),
    )
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, blank=True
    )
    email = models.EmailField(_("Email"), blank=True)
    address = models.TextField(_("Address"), blank=True)
    city = models.CharField(_("City"), max_length=100, blank=True, default="")
    postal_code = models.CharField(_("Postal Code"), max_length=20, blank=True)

    # Additional Information
    occupation = models.CharField(_("Occupation"), max_length=200, blank=True)
    photo = models.ImageField(
        _("Photo"), upload_to="citizens/photos/", blank=True, null=True
    )
    notes = models.TextField(_("Notes"), blank=True)

    # System Fields
    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="citizen_profile",
        verbose_name=_("User Account"),
        help_text=_("Link to user account for citizen login"),
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="citizens_created",
        verbose_name=_("Created By"),
    )
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
    is_active = models.BooleanField(_("Is Active"), default=True)

    class Meta:
        verbose_name = _("Citizen")
        verbose_name_plural = _("Citizens")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["national_id"]),
            models.Index(fields=["last_name", "first_name"]),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.national_id})"

    @property
    def full_name(self):
        """Return the full name of the citizen."""
        if self.middle_name:
            return f"{self.first_name} {self.middle_name} {self.last_name}"
        return f"{self.first_name} {self.last_name}"


class CitizenDocument(models.Model):
    """Model for storing citizen documents."""

    DOCUMENT_TYPE_CHOICES = [
        ("ID", _("National ID")),
        ("PASSPORT", _("Passport")),
        ("BIRTH_CERT", _("Birth Certificate")),
        ("MARRIAGE_CERT", _("Marriage Certificate")),
        ("OTHER", _("Other")),
    ]

    citizen = models.ForeignKey(
        Citizen, on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(
        _("Document Type"), max_length=20, choices=DOCUMENT_TYPE_CHOICES
    )
    document_number = models.CharField(_("Document Number"), max_length=100)
    file = models.FileField(_("Document File"), upload_to="citizens/documents/")
    issue_date = models.DateField(_("Issue Date"), blank=True, null=True)
    expiry_date = models.DateField(_("Expiry Date"), blank=True, null=True)
    description = models.TextField(_("Description"), blank=True)
    uploaded_at = models.DateTimeField(_("Uploaded At"), auto_now_add=True)

    class Meta:
        verbose_name = _("Citizen Document")
        verbose_name_plural = _("Citizen Documents")
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.citizen.full_name} - {self.get_document_type_display()}"
