"""
Views for Officer role - Officers can approve holding taxes and certificates.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from citizen.decorators import officer_required
from holdingtax.models import HoldingTax
from certification.models import Certification
from tradelicense.models import TradeLicense


@officer_required
def officer_dashboard(request):
    """Officer dashboard showing items pending approval."""
    # Pending holding taxes
    pending_taxes = HoldingTax.objects.filter(status='PENDING').count()
    
    # Pending certifications
    pending_certifications = Certification.objects.filter(status='pending').count()
    
    # Pending trade licenses
    pending_licenses = TradeLicense.objects.filter(status='pending').count()
    
    # Recent pending items
    recent_taxes = HoldingTax.objects.filter(status='PENDING').order_by('-created_at')[:5]
    recent_certifications = Certification.objects.filter(status='pending').order_by('-created_at')[:5]
    recent_licenses = TradeLicense.objects.filter(status='pending').order_by('-created_at')[:5]
    
    context = {
        'pending_taxes': pending_taxes,
        'pending_certifications': pending_certifications,
        'pending_licenses': pending_licenses,
        'recent_taxes': recent_taxes,
        'recent_certifications': recent_certifications,
        'recent_licenses': recent_licenses,
    }
    
    return render(request, 'officer/dashboard.html', context)


@officer_required
def officer_holdingtax_list(request):
    """List holding taxes pending approval."""
    holding_taxes = HoldingTax.objects.filter(status='PENDING').order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        holding_taxes = holding_taxes.filter(
            Q(tax_number__icontains=search_query) |
            Q(holding_property__property_number__icontains=search_query) |
            Q(holding_property__owner__first_name__icontains=search_query) |
            Q(holding_property__owner__last_name__icontains=search_query)
        )
    
    paginator = Paginator(holding_taxes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'officer/holdingtax_list.html', context)


@officer_required
def officer_holdingtax_approve(request, pk):
    """Approve a holding tax."""
    holding_tax = get_object_or_404(HoldingTax, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            holding_tax.status = 'PAID'  # Or whatever status you want for approved
            holding_tax.save()
            messages.success(request, f'Holding Tax {holding_tax.tax_number} approved successfully!')
        elif action == 'reject':
            holding_tax.status = 'OVERDUE'  # Or add a rejected status
            holding_tax.save()
            messages.success(request, f'Holding Tax {holding_tax.tax_number} rejected.')
        
        return redirect('officer:holdingtax_list')
    
    context = {
        'holding_tax': holding_tax,
    }
    
    return render(request, 'officer/holdingtax_approve.html', context)


@officer_required
def officer_certification_list(request):
    """List certifications pending approval."""
    certifications = Certification.objects.filter(status='pending').order_by('-created_at')
    
    search_query = request.GET.get('search', '')
    if search_query:
        certifications = certifications.filter(
            Q(certificate_number__icontains=search_query) |
            Q(citizen__first_name__icontains=search_query) |
            Q(citizen__last_name__icontains=search_query) |
            Q(certification_type__name__icontains=search_query)
        )
    
    paginator = Paginator(certifications, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'officer/certification_list.html', context)


@officer_required
def officer_certification_approve(request, pk):
    """Approve a certification."""
    certification = get_object_or_404(Certification, pk=pk)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            certification.status = 'approved'
            certification.issue_date = timezone.now().date()
            certification.expiry_date = certification.issue_date + timedelta(days=certification.certification_type.validity_days)
            certification.issued_by = request.user
            certification.save()
            messages.success(request, f'Certification {certification.certificate_number} approved successfully!')
        elif action == 'reject':
            certification.status = 'rejected'
            certification.rejection_reason = request.POST.get('rejection_reason', '')
            certification.save()
            messages.success(request, f'Certification {certification.certificate_number} rejected.')
        
        return redirect('officer:certification_list')
    
    context = {
        'certification': certification,
    }
    
    return render(request, 'officer/certification_approve.html', context)
