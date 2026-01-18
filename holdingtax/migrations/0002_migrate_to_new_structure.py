# Generated manually

from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings
from decimal import Decimal
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('holdingtax', '0001_initial'),
        ('citizen', '0002_citizendocument_remove_citizen_nid_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # Drop old HoldingTax table
        migrations.DeleteModel(
            name='HoldingTax',
        ),
        # Create new models
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Area Name')),
                ('code', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Area Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Area',
                'verbose_name_plural': 'Areas',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AttachmentType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Attachment Type Name')),
                ('code', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Attachment Type Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Attachment Type',
                'verbose_name_plural': 'Attachment Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='PropertyType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Property Type Name')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Property Type Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Property Type',
                'verbose_name_plural': 'Property Types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TaxPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Period Name')),
                ('start_date', models.DateField(verbose_name='Start Date')),
                ('end_date', models.DateField(verbose_name='End Date')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
            ],
            options={
                'verbose_name': 'Tax Period',
                'verbose_name_plural': 'Tax Periods',
                'ordering': ['-start_date'],
            },
        ),
        migrations.CreateModel(
            name='Street',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Street Name')),
                ('code', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Street Code')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='streets', to='holdingtax.area')),
            ],
            options={
                'verbose_name': 'Street',
                'verbose_name_plural': 'Streets',
                'ordering': ['area', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_number', models.CharField(max_length=50, unique=True, verbose_name='Holding Number')),
                ('address', models.TextField(help_text='Detailed address (house number, building name, etc.)', verbose_name='Property Address')),
                ('city', models.CharField(blank=True, max_length=100, verbose_name='City')),
                ('postal_code', models.CharField(blank=True, max_length=20, verbose_name='Postal Code')),
                ('area_sqft', models.DecimalField(decimal_places=2, help_text='Total area in square feet', max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Area (sq ft)')),
                ('assessed_value', models.DecimalField(decimal_places=2, help_text='Assessed property value', max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Assessed Value')),
                ('tax_rate', models.DecimalField(decimal_places=2, default=Decimal('0.00'), help_text='Tax rate as percentage', max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Tax Rate (%)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING_APPROVAL', 'Pending Approval'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')], default='DRAFT', help_text='Workflow status of the holding', max_length=20, verbose_name='Status')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('submitted_at', models.DateTimeField(blank=True, help_text='When the holding was submitted for approval', null=True, verbose_name='Submitted At')),
                ('approved_at', models.DateTimeField(blank=True, help_text='When the holding was approved', null=True, verbose_name='Approved At')),
                ('rejection_reason', models.TextField(blank=True, help_text='Reason for rejection if applicable', verbose_name='Rejection Reason')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='properties', to='holdingtax.area')),
                ('approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='properties_approved', to=settings.AUTH_USER_MODEL, verbose_name='Approved By')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='properties_created', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='properties', to='citizen.citizen')),
                ('property_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='properties', to='holdingtax.propertytype')),
                ('street', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='properties', to='holdingtax.street')),
                ('submitted_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='properties_submitted', to=settings.AUTH_USER_MODEL, verbose_name='Submitted By')),
            ],
            options={
                'verbose_name': 'Holding',
                'verbose_name_plural': 'Holdings',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='HoldingTax',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tax_number', models.CharField(max_length=50, unique=True, verbose_name='Tax Number')),
                ('tax_amount', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Tax Amount')),
                ('paid_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Paid Amount')),
                ('due_date', models.DateField(verbose_name='Due Date')),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('PAID', 'Paid'), ('PARTIAL', 'Partially Paid'), ('OVERDUE', 'Overdue'), ('WAIVED', 'Waived')], default='PENDING', max_length=20, verbose_name='Status')),
                ('penalty_amount', models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))], verbose_name='Penalty Amount')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='holding_taxes_created', to=settings.AUTH_USER_MODEL)),
                ('holding_property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='holding_taxes', to='holdingtax.property')),
                ('tax_period', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='holding_taxes', to='holdingtax.taxperiod')),
            ],
            options={
                'verbose_name': 'Holding Tax',
                'verbose_name_plural': 'Holding Taxes',
                'ordering': ['-due_date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='TaxPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_number', models.CharField(max_length=50, unique=True, verbose_name='Payment Number')),
                ('payment_date', models.DateField(verbose_name='Payment Date')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))], verbose_name='Amount')),
                ('payment_method', models.CharField(choices=[('CASH', 'Cash'), ('CHEQUE', 'Cheque'), ('BANK_TRANSFER', 'Bank Transfer'), ('ONLINE', 'Online Payment'), ('OTHER', 'Other')], max_length=20, verbose_name='Payment Method')),
                ('reference_number', models.CharField(blank=True, max_length=100, verbose_name='Reference Number')),
                ('cheque_number', models.CharField(blank=True, max_length=50, verbose_name='Cheque Number')),
                ('bank_name', models.CharField(blank=True, max_length=100, verbose_name='Bank Name')),
                ('notes', models.TextField(blank=True, verbose_name='Notes')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('holding_tax', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payments', to='holdingtax.holdingtax')),
                ('received_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tax_payments_received', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Tax Payment',
                'verbose_name_plural': 'Tax Payments',
                'ordering': ['-payment_date', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PropertyAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, verbose_name='Title')),
                ('description', models.TextField(blank=True, verbose_name='Description')),
                ('file', models.FileField(upload_to='property_attachments/%Y/%m/%d/', verbose_name='File')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True, verbose_name='Uploaded At')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('attachment_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='attachments', to='holdingtax.attachmenttype')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='holdingtax.property')),
                ('uploaded_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='property_attachments_uploaded', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Property Attachment',
                'verbose_name_plural': 'Property Attachments',
                'ordering': ['-uploaded_at'],
            },
        ),
        migrations.AddIndex(
            model_name='area',
            index=models.Index(fields=['name'], name='holdingtax_a_name_idx'),
        ),
        migrations.AddIndex(
            model_name='street',
            index=models.Index(fields=['name'], name='holdingtax_s_name_idx'),
        ),
        migrations.AddIndex(
            model_name='street',
            index=models.Index(fields=['area'], name='holdingtax_s_area_id_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['property_number'], name='holdingtax_p_property_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['owner'], name='holdingtax_p_owner_id_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['city'], name='holdingtax_p_city_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['area'], name='holdingtax_p_area_id_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['street'], name='holdingtax_p_street_idx'),
        ),
        migrations.AddIndex(
            model_name='property',
            index=models.Index(fields=['status'], name='holdingtax_p_status_idx'),
        ),
        migrations.AddIndex(
            model_name='holdingtax',
            index=models.Index(fields=['tax_number'], name='holdingtax_h_tax_num_idx'),
        ),
        migrations.AddIndex(
            model_name='holdingtax',
            index=models.Index(fields=['holding_property'], name='holdingtax_h_holding_idx'),
        ),
        migrations.AddIndex(
            model_name='holdingtax',
            index=models.Index(fields=['status'], name='holdingtax_h_status_idx'),
        ),
        migrations.AddIndex(
            model_name='holdingtax',
            index=models.Index(fields=['due_date'], name='holdingtax_h_due_dat_idx'),
        ),
        migrations.AddIndex(
            model_name='propertyattachment',
            index=models.Index(fields=['property'], name='holdingtax_pa_property_idx'),
        ),
        migrations.AddIndex(
            model_name='propertyattachment',
            index=models.Index(fields=['attachment_type'], name='holdingtax_pa_attachm_idx'),
        ),
        migrations.AddIndex(
            model_name='propertyattachment',
            index=models.Index(fields=['uploaded_at'], name='holdingtax_pa_uploaded_idx'),
        ),
        migrations.AddIndex(
            model_name='taxpayment',
            index=models.Index(fields=['payment_date'], name='holdingtax_t_payment_idx'),
        ),
        migrations.AddIndex(
            model_name='taxpayment',
            index=models.Index(fields=['holding_tax'], name='holdingtax_t_holding_idx'),
        ),
    ]
