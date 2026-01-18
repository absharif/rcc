from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from datetime import timedelta
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from .models import Certification, CertificationType
from .forms import CertificationForm, CertificationTypeForm


@login_required
def certification_list(request):
    """List all certifications with search and pagination."""
    certifications = Certification.objects.select_related('citizen', 'certification_type').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    
    if search_query:
        certifications = certifications.filter(
            Q(certificate_number__icontains=search_query) |
            Q(citizen__first_name__icontains=search_query) |
            Q(citizen__last_name__icontains=search_query) |
            Q(citizen__national_id__icontains=search_query)
        )
    
    if status_filter:
        certifications = certifications.filter(status=status_filter)
    
    if type_filter:
        certifications = certifications.filter(certification_type_id=type_filter)
    
    # Pagination
    paginator = Paginator(certifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_certifications = certifications.count()
    pending_count = certifications.filter(status='pending').count()
    approved_count = certifications.filter(status='approved').count()
    rejected_count = certifications.filter(status='rejected').count()
    
    # Get certification types for filter
    certification_types = CertificationType.objects.filter(is_active=True)
    
    context = {
        'certifications': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'total_count': total_certifications,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'certification_types': certification_types,
    }
    return render(request, 'certification/list.html', context)


@login_required
def certification_detail(request, pk):
    """View certification details."""
    certification = get_object_or_404(
        Certification.objects.select_related('citizen', 'certification_type', 'created_by', 'issued_by'),
        pk=pk
    )
    
    context = {
        'certification': certification,
        'is_expired': certification.is_expired(),
        'is_valid': certification.is_valid(),
    }
    return render(request, 'certification/detail.html', context)


@login_required
def certification_create(request):
    """Create a new certification."""
    if request.method == 'POST':
        form = CertificationForm(request.POST)
        if form.is_valid():
            certification = form.save(commit=False)
            certification.created_by = request.user
            certification.save()
            messages.success(request, f'Certification {certification.certificate_number} created successfully!')
            return redirect('certification:detail', pk=certification.pk)
    else:
        form = CertificationForm()
    
    context = {
        'form': form,
        'title': 'Add New Certification',
    }
    return render(request, 'certification/form.html', context)


@login_required
def certification_update(request, pk):
    """Update an existing certification."""
    certification = get_object_or_404(Certification, pk=pk)
    
    if request.method == 'POST':
        form = CertificationForm(request.POST, instance=certification)
        if form.is_valid():
            form.save()
            messages.success(request, f'Certification {certification.certificate_number} updated successfully!')
            return redirect('certification:detail', pk=certification.pk)
    else:
        form = CertificationForm(instance=certification)
    
    context = {
        'form': form,
        'certification': certification,
        'title': 'Update Certification',
    }
    return render(request, 'certification/form.html', context)


@login_required
def certification_delete(request, pk):
    """Delete a certification."""
    certification = get_object_or_404(Certification, pk=pk)
    
    if request.method == 'POST':
        certificate_number = certification.certificate_number
        certification.delete()
        messages.success(request, f'Certification {certificate_number} deleted successfully!')
        return redirect('certification:list')
    
    context = {
        'certification': certification,
    }
    return render(request, 'certification/delete.html', context)


@login_required
def generate_pdf(request, pk):
    """Generate PDF certificate for a certification."""
    certification = get_object_or_404(
        Certification.objects.select_related('citizen', 'certification_type'),
        pk=pk
    )
    
    if certification.status != 'approved':
        messages.error(request, 'Only approved certifications can generate PDF certificates.')
        return redirect('certification:detail', pk=pk)
    
    # Create PDF buffer
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Container for the 'Flowable' objects
    elements = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a365d'),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        textColor=colors.HexColor('#2d3748'),
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor('#4a5568'),
        alignment=TA_LEFT,
        spaceAfter=12
    )
    
    # Certificate Title
    elements.append(Paragraph("CERTIFICATE", title_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Certificate Type
    elements.append(Paragraph(f"{certification.certification_type.name.upper()}", heading_style))
    elements.append(Spacer(1, 0.4*inch))
    
    # Certificate Number
    elements.append(Paragraph(f"Certificate No: {certification.certificate_number}", normal_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Main content
    content_text = f"""
    This is to certify that <b>{certification.citizen.full_name}</b>, 
    National ID: <b>{certification.citizen.national_id or 'N/A'}</b>,
    """
    
    if certification.citizen.date_of_birth:
        content_text += f"Date of Birth: <b>{certification.citizen.date_of_birth.strftime('%B %d, %Y')}</b>, "
    
    if certification.citizen.address:
        content_text += f"Residing at <b>{certification.citizen.address}</b>, "
    
    content_text += f"is hereby issued this {certification.certification_type.name}."
    
    elements.append(Paragraph(content_text, normal_style))
    elements.append(Spacer(1, 0.3*inch))
    
    # Additional remarks if any
    if certification.remarks:
        elements.append(Paragraph(f"Remarks: {certification.remarks}", normal_style))
        elements.append(Spacer(1, 0.2*inch))
    
    # Issue date
    issue_date = certification.issue_date or timezone.now().date()
    elements.append(Paragraph(f"Issued on: {issue_date.strftime('%B %d, %Y')}", normal_style))
    
    # Expiry date if available
    if certification.expiry_date:
        elements.append(Paragraph(f"Valid until: {certification.expiry_date.strftime('%B %d, %Y')}", normal_style))
    
    elements.append(Spacer(1, 0.5*inch))
    
    # Signature section
    signature_data = [
        ['', ''],
        ['', ''],
        ['', ''],
    ]
    
    signature_table = Table(signature_data, colWidths=[3*inch, 3*inch])
    signature_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'BOTTOM'),
    ]))
    elements.append(signature_table)
    elements.append(Spacer(1, 0.2*inch))
    
    # Signature labels
    signature_labels = [
        ['Authorized Signatory', 'City Corporation']
    ]
    signature_label_table = Table(signature_labels, colWidths=[3*inch, 3*inch])
    signature_label_table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
    ]))
    elements.append(signature_label_table)
    
    # Build PDF
    doc.build(elements)
    
    # Get PDF value
    pdf = buffer.getvalue()
    buffer.close()
    
    # Save PDF to model if not already saved
    if not certification.pdf_file:
        from django.core.files.base import ContentFile
        filename = f"certificate_{certification.certificate_number}.pdf"
        certification.pdf_file.save(filename, ContentFile(pdf), save=True)
        certification.issued_by = request.user
        if not certification.issue_date:
            certification.issue_date = timezone.now().date()
        certification.save()
    
    # Return PDF response
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{certification.certificate_number}.pdf"'
    return response


@login_required
def approve_certification(request, pk):
    """Approve a certification."""
    certification = get_object_or_404(Certification, pk=pk)
    
    if request.method == 'POST':
        certification.status = 'approved'
        certification.issued_by = request.user
        if not certification.issue_date:
            certification.issue_date = timezone.now().date()
        
        # Set expiry date based on certification type validity
        if certification.certification_type.validity_days and not certification.expiry_date:
            certification.expiry_date = certification.issue_date + timedelta(days=certification.certification_type.validity_days)
        
        certification.save()
        messages.success(request, f'Certification {certification.certificate_number} approved successfully!')
        return redirect('certification:detail', pk=pk)
    
    return redirect('certification:detail', pk=pk)
