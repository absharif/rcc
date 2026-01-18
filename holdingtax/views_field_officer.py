"""
Views for Holding Tax Field Officer role.
Field officers can add citizens, create properties, and create holding taxes.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from citizen.decorators import field_officer_required
from citizen.models import Citizen
from citizen.forms import CitizenForm
from .models import Area, Street, PropertyType, Property, TaxPeriod, HoldingTax
from .forms import PropertyForm, HoldingTaxForm


@field_officer_required
def field_officer_dashboard(request):
    """Field Officer dashboard."""
    # Statistics
    citizens_count = Citizen.objects.count()
    properties_count = Property.objects.count()
    holding_taxes_count = HoldingTax.objects.count()
    pending_taxes = HoldingTax.objects.filter(status='PENDING').count()
    
    # Recent activities
    recent_citizens = Citizen.objects.order_by('-created_at')[:5]
    recent_properties = Property.objects.order_by('-created_at')[:5]
    recent_taxes = HoldingTax.objects.order_by('-created_at')[:5]
    
    context = {
        'citizens_count': citizens_count,
        'properties_count': properties_count,
        'holding_taxes_count': holding_taxes_count,
        'pending_taxes': pending_taxes,
        'recent_citizens': recent_citizens,
        'recent_properties': recent_properties,
        'recent_taxes': recent_taxes,
    }
    
    return render(request, 'field_officer/dashboard.html', context)


@field_officer_required
def field_officer_citizen_list(request):
    """List citizens - Field Officer can view all."""
    citizens = Citizen.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        citizens = citizens.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(national_id__icontains=search_query) |
            Q(phone_number__icontains=search_query)
        )
    
    paginator = Paginator(citizens, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'field_officer/citizen_list.html', context)


@field_officer_required
def field_officer_citizen_create(request):
    """Create a new citizen."""
    if request.method == 'POST':
        form = CitizenForm(request.POST, request.FILES)
        if form.is_valid():
            citizen = form.save(commit=False)
            citizen.created_by = request.user
            citizen.save()
            messages.success(request, f'Citizen {citizen.full_name} created successfully!')
            return redirect('field_officer:citizen_list')
    else:
        form = CitizenForm()
    
    context = {
        'form': form,
        'title': 'Add New Citizen',
    }
    
    return render(request, 'field_officer/citizen_form.html', context)


@field_officer_required
def field_officer_property_list(request):
    """List properties."""
    properties = Property.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        properties = properties.filter(
            Q(property_number__icontains=search_query) |
            Q(holding_number__icontains=search_query) |
            Q(owner__first_name__icontains=search_query) |
            Q(owner__last_name__icontains=search_query)
        )
    
    paginator = Paginator(properties, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    
    return render(request, 'field_officer/property_list.html', context)


@field_officer_required
def field_officer_property_create(request):
    """Create a new property."""
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property = form.save(commit=False)
            property.created_by = request.user
            property.save()
            messages.success(request, f'Property {property.property_number} created successfully!')
            return redirect('field_officer:property_list')
    else:
        form = PropertyForm()
    
    context = {
        'form': form,
        'title': 'Add New Property',
    }
    
    return render(request, 'field_officer/property_form.html', context)


@field_officer_required
def field_officer_holdingtax_list(request):
    """List holding taxes."""
    holding_taxes = HoldingTax.objects.all()
    
    search_query = request.GET.get('search', '')
    if search_query:
        holding_taxes = holding_taxes.filter(
            Q(tax_number__icontains=search_query) |
            Q(holding_property__property_number__icontains=search_query) |
            Q(holding_property__owner__first_name__icontains=search_query) |
            Q(holding_property__owner__last_name__icontains=search_query)
        )
    
    status_filter = request.GET.get('status', '')
    if status_filter:
        holding_taxes = holding_taxes.filter(status=status_filter)
    
    paginator = Paginator(holding_taxes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
    }
    
    return render(request, 'field_officer/holdingtax_list.html', context)


@field_officer_required
def field_officer_holdingtax_create(request):
    """Create a new holding tax."""
    if request.method == 'POST':
        form = HoldingTaxForm(request.POST)
        if form.is_valid():
            holding_tax = form.save()
            messages.success(request, f'Holding Tax {holding_tax.tax_number} created successfully!')
            return redirect('field_officer:holdingtax_list')
    else:
        form = HoldingTaxForm()
    
    context = {
        'form': form,
        'title': 'Add New Holding Tax',
    }
    
    return render(request, 'field_officer/holdingtax_form.html', context)
