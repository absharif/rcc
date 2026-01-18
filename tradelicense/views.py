from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import date
from .models import TradeLicense
from .forms import TradeLicenseForm


@login_required
def trade_license_list(request):
    """List all trade licenses with search and pagination."""
    trade_licenses = TradeLicense.objects.select_related('citizen').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        trade_licenses = trade_licenses.filter(
            Q(license_number__icontains=search_query) |
            Q(business_name__icontains=search_query) |
            Q(business_type__icontains=search_query) |
            Q(citizen__first_name__icontains=search_query) |
            Q(citizen__last_name__icontains=search_query) |
            Q(citizen__national_id__icontains=search_query)
        )
    
    if status_filter:
        trade_licenses = trade_licenses.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(trade_licenses, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_licenses = trade_licenses.count()
    total_fee = trade_licenses.aggregate(Sum('license_fee'))['license_fee__sum'] or 0
    pending_count = trade_licenses.filter(status='pending').count()
    approved_count = trade_licenses.filter(status='approved').count()
    expired_count = trade_licenses.filter(status='expired').count()
    
    # Check for expired licenses
    today = date.today()
    expired_licenses = trade_licenses.filter(expiry_date__lt=today).exclude(status='expired').count()
    
    context = {
        'trade_licenses': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': total_licenses,
        'total_fee': total_fee,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'expired_count': expired_count,
        'expired_licenses': expired_licenses,
    }
    return render(request, 'tradelicense/list.html', context)


@login_required
def trade_license_detail(request, pk):
    """View trade license details."""
    trade_license = get_object_or_404(TradeLicense.objects.select_related('citizen'), pk=pk)
    
    # Check if expired
    is_expired = trade_license.expiry_date < date.today() and trade_license.status != 'expired'
    
    context = {
        'trade_license': trade_license,
        'is_expired': is_expired,
    }
    return render(request, 'tradelicense/detail.html', context)


@login_required
def trade_license_create(request):
    """Create a new trade license."""
    if request.method == 'POST':
        form = TradeLicenseForm(request.POST)
        if form.is_valid():
            trade_license = form.save()
            messages.success(request, f'Trade License {trade_license.license_number} created successfully!')
            return redirect('tradelicense:detail', pk=trade_license.pk)
    else:
        form = TradeLicenseForm()
    
    context = {
        'form': form,
        'title': 'Add New Trade License',
    }
    return render(request, 'tradelicense/form.html', context)


@login_required
def trade_license_update(request, pk):
    """Update an existing trade license."""
    trade_license = get_object_or_404(TradeLicense, pk=pk)
    
    if request.method == 'POST':
        form = TradeLicenseForm(request.POST, instance=trade_license)
        if form.is_valid():
            form.save()
            messages.success(request, f'Trade License {trade_license.license_number} updated successfully!')
            return redirect('tradelicense:detail', pk=trade_license.pk)
    else:
        form = TradeLicenseForm(instance=trade_license)
    
    context = {
        'form': form,
        'trade_license': trade_license,
        'title': 'Update Trade License',
    }
    return render(request, 'tradelicense/form.html', context)


@login_required
def trade_license_delete(request, pk):
    """Delete a trade license."""
    trade_license = get_object_or_404(TradeLicense, pk=pk)
    
    if request.method == 'POST':
        license_number = trade_license.license_number
        trade_license.delete()
        messages.success(request, f'Trade License {license_number} deleted successfully!')
        return redirect('tradelicense:list')
    
    context = {
        'trade_license': trade_license,
    }
    return render(request, 'tradelicense/delete.html', context)
