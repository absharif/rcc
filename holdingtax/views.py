from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone
from decimal import Decimal
from .models import (
    Area, Street, PropertyType, Property, TaxPeriod,
    HoldingTax, AttachmentType, PropertyAttachment, TaxPayment
)
from .forms import (
    AreaForm, StreetForm, PropertyTypeForm, PropertyForm,
    TaxPeriodForm, HoldingTaxForm, TaxPaymentForm, PropertyAttachmentForm
)


@login_required
def holding_tax_list(request):
    """List all holding taxes with search and pagination."""
    holding_taxes = HoldingTax.objects.select_related('holding_property', 'tax_period', 'holding_property__owner').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        holding_taxes = holding_taxes.filter(
            Q(tax_number__icontains=search_query) |
            Q(holding_property__property_number__icontains=search_query) |
            Q(holding_property__owner__first_name__icontains=search_query) |
            Q(holding_property__owner__last_name__icontains=search_query) |
            Q(holding_property__owner__national_id__icontains=search_query)
        )
    
    if status_filter:
        holding_taxes = holding_taxes.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(holding_taxes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_tax = holding_taxes.aggregate(Sum('tax_amount'))['tax_amount__sum'] or Decimal('0.00')
    total_paid = holding_taxes.aggregate(Sum('paid_amount'))['paid_amount__sum'] or Decimal('0.00')
    total_pending = holding_taxes.filter(status='PENDING').count()
    total_overdue = holding_taxes.filter(status='OVERDUE').count()
    
    context = {
        'holding_taxes': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': holding_taxes.count(),
        'total_tax': total_tax,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'total_overdue': total_overdue,
    }
    return render(request, 'holdingtax/list.html', context)


@login_required
def holding_tax_detail(request, pk):
    """View holding tax details."""
    holding_tax = get_object_or_404(HoldingTax.objects.select_related('holding_property', 'tax_period'), pk=pk)
    payments = holding_tax.payments.all().order_by('-payment_date')
    total_paid = payments.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
    
    context = {
        'holding_tax': holding_tax,
        'payments': payments,
        'total_paid': total_paid,
        'balance': holding_tax.balance_amount,
    }
    return render(request, 'holdingtax/detail.html', context)


@login_required
def holding_tax_create(request):
    """Create a new holding tax."""
    if request.method == 'POST':
        form = HoldingTaxForm(request.POST)
        if form.is_valid():
            holding_tax = form.save(commit=False)
            holding_tax.created_by = request.user
            holding_tax.save()
            messages.success(request, f'Holding Tax {holding_tax.tax_number} created successfully!')
            return redirect('holdingtax:detail', pk=holding_tax.pk)
    else:
        form = HoldingTaxForm()
    
    context = {
        'form': form,
        'title': 'Add New Holding Tax',
    }
    return render(request, 'holdingtax/form.html', context)


@login_required
def holding_tax_update(request, pk):
    """Update an existing holding tax."""
    holding_tax = get_object_or_404(HoldingTax, pk=pk)
    
    if request.method == 'POST':
        form = HoldingTaxForm(request.POST, instance=holding_tax)
        if form.is_valid():
            form.save()
            messages.success(request, f'Holding Tax {holding_tax.tax_number} updated successfully!')
            return redirect('holdingtax:detail', pk=holding_tax.pk)
    else:
        form = HoldingTaxForm(instance=holding_tax)
    
    context = {
        'form': form,
        'holding_tax': holding_tax,
        'title': 'Update Holding Tax',
    }
    return render(request, 'holdingtax/form.html', context)


@login_required
def holding_tax_delete(request, pk):
    """Delete a holding tax."""
    holding_tax = get_object_or_404(HoldingTax, pk=pk)
    
    if request.method == 'POST':
        tax_number = holding_tax.tax_number
        holding_tax.delete()
        messages.success(request, f'Holding Tax {tax_number} deleted successfully!')
        return redirect('holdingtax:list')
    
    context = {
        'holding_tax': holding_tax,
    }
    return render(request, 'holdingtax/delete.html', context)


@login_required
def property_list(request):
    """List all properties."""
    properties = Property.objects.select_related('owner', 'property_type', 'area', 'street').filter(is_active=True)
    
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        properties = properties.filter(
            Q(property_number__icontains=search_query) |
            Q(owner__first_name__icontains=search_query) |
            Q(owner__last_name__icontains=search_query) |
            Q(owner__national_id__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    if status_filter:
        properties = properties.filter(status=status_filter)
    
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'properties': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': properties.count(),
    }
    return render(request, 'holdingtax/property_list.html', context)


@login_required
def property_detail(request, pk):
    """View property details."""
    property_obj = get_object_or_404(Property.objects.select_related('owner', 'property_type', 'area', 'street'), pk=pk)
    holding_taxes = property_obj.holding_taxes.all().order_by('-due_date')
    attachments = property_obj.attachments.filter(is_active=True)
    
    context = {
        'property': property_obj,
        'holding_taxes': holding_taxes,
        'attachments': attachments,
    }
    return render(request, 'holdingtax/property_detail.html', context)


@login_required
def property_create(request):
    """Create a new property."""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.created_by = request.user
            property_obj.save()
            messages.success(request, f'Property {property_obj.property_number} created successfully!')
            return redirect('holdingtax:property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm()
    
    context = {
        'form': form,
        'title': 'Add New Property',
    }
    return render(request, 'holdingtax/property_form.html', context)


@login_required
def property_update(request, pk):
    """Update an existing property."""
    property_obj = get_object_or_404(Property, pk=pk)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Property {property_obj.property_number} updated successfully!')
            return redirect('holdingtax:property_detail', pk=property_obj.pk)
    else:
        form = PropertyForm(instance=property_obj)
    
    context = {
        'form': form,
        'property': property_obj,
        'title': 'Update Property',
    }
    return render(request, 'holdingtax/property_form.html', context)


@login_required
def tax_payment_add(request, holding_tax_pk):
    """Add a payment to a holding tax."""
    holding_tax = get_object_or_404(HoldingTax, pk=holding_tax_pk)
    
    if request.method == 'POST':
        form = TaxPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.holding_tax = holding_tax
            payment.received_by = request.user
            payment.save()
            
            # Update holding tax paid amount
            total_paid = holding_tax.payments.aggregate(Sum('amount'))['amount__sum'] or Decimal('0.00')
            holding_tax.paid_amount = total_paid
            
            # Update status
            if total_paid >= holding_tax.tax_amount + holding_tax.penalty_amount:
                holding_tax.status = 'PAID'
            elif total_paid > Decimal('0.00'):
                holding_tax.status = 'PARTIAL'
            holding_tax.save()
            
            messages.success(request, 'Payment recorded successfully!')
            return redirect('holdingtax:detail', pk=holding_tax.pk)
    else:
        form = TaxPaymentForm(initial={'holding_tax': holding_tax})
    
    context = {
        'form': form,
        'holding_tax': holding_tax,
        'title': 'Add Payment',
    }
    return render(request, 'holdingtax/payment_form.html', context)
