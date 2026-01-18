"""
Views for Citizen role - citizens can view their own data.
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .decorators import citizen_required
from .models import Citizen
from holdingtax.models import Property, HoldingTax
from tradelicense.models import TradeLicense
from certification.models import Certification


@citizen_required
def citizen_dashboard(request):
    """Citizen dashboard showing their own data."""
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        messages.error(request, 'No citizen profile linked to your account. Please contact administrator.')
        return redirect('home')
    
    # Get citizen's properties
    properties = Property.objects.filter(owner=citizen)
    
    # Get citizen's holding taxes
    holding_taxes = HoldingTax.objects.filter(holding_property__owner=citizen).order_by('-created_at')
    
    # Get citizen's trade licenses
    trade_licenses = TradeLicense.objects.filter(citizen=citizen).order_by('-created_at')
    
    # Get citizen's certifications
    certifications = Certification.objects.filter(citizen=citizen).order_by('-created_at')
    
    # Statistics
    stats = {
        'properties_count': properties.count(),
        'holding_taxes_count': holding_taxes.count(),
        'pending_taxes': holding_taxes.filter(status='PENDING').count(),
        'paid_taxes': holding_taxes.filter(status='PAID').count(),
        'overdue_taxes': holding_taxes.filter(status='OVERDUE').count(),
        'trade_licenses_count': trade_licenses.count(),
        'active_licenses': trade_licenses.filter(status='approved').count(),
        'certifications_count': certifications.count(),
        'approved_certifications': certifications.filter(status='approved').count(),
    }
    
    context = {
        'citizen': citizen,
        'properties': properties[:5],  # Show latest 5
        'holding_taxes': holding_taxes[:5],  # Show latest 5
        'trade_licenses': trade_licenses[:5],  # Show latest 5
        'certifications': certifications[:5],  # Show latest 5
        'stats': stats,
    }
    
    return render(request, 'citizen/dashboard.html', context)


@citizen_required
def citizen_properties(request):
    """Citizen's properties list."""
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'No citizen profile linked to your account.')
        return redirect('citizen:dashboard')
    
    properties = Property.objects.filter(owner=citizen)
    
    context = {
        'citizen': citizen,
        'properties': properties,
    }
    
    return render(request, 'citizen/properties.html', context)


@citizen_required
def citizen_holding_taxes(request):
    """Citizen's holding taxes list."""
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'No citizen profile linked to your account.')
        return redirect('citizen:dashboard')
    
    holding_taxes = HoldingTax.objects.filter(holding_property__owner=citizen).order_by('-created_at')
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        holding_taxes = holding_taxes.filter(status=status_filter)
    
    context = {
        'citizen': citizen,
        'holding_taxes': holding_taxes,
        'status_filter': status_filter,
    }
    
    return render(request, 'citizen/holding_taxes.html', context)


@citizen_required
def citizen_trade_licenses(request):
    """Citizen's trade licenses list."""
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'No citizen profile linked to your account.')
        return redirect('citizen:dashboard')
    
    trade_licenses = TradeLicense.objects.filter(citizen=citizen).order_by('-created_at')
    
    context = {
        'citizen': citizen,
        'trade_licenses': trade_licenses,
    }
    
    return render(request, 'citizen/trade_licenses.html', context)


@citizen_required
def citizen_certifications(request):
    """Citizen's certifications list."""
    try:
        citizen = request.user.citizen_profile
    except Citizen.DoesNotExist:
        from django.contrib import messages
        from django.shortcuts import redirect
        messages.error(request, 'No citizen profile linked to your account.')
        return redirect('citizen:dashboard')
    
    certifications = Certification.objects.filter(citizen=citizen).order_by('-created_at')
    
    context = {
        'citizen': citizen,
        'certifications': certifications,
    }
    
    return render(request, 'citizen/certifications.html', context)
