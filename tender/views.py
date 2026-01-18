from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import datetime
from .models import Tender
from .forms import TenderForm


@login_required
def tender_list(request):
    """List all tenders with search and pagination."""
    tenders = Tender.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    if search_query:
        tenders = tenders.filter(
            Q(tender_number__icontains=search_query) |
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    if status_filter:
        tenders = tenders.filter(status=status_filter)
    
    # Pagination
    paginator = Paginator(tenders, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_tenders = tenders.count()
    draft_count = tenders.filter(status='draft').count()
    published_count = tenders.filter(status='published').count()
    closed_count = tenders.filter(status='closed').count()
    awarded_count = tenders.filter(status='awarded').count()
    
    # Check for upcoming/closing tenders
    now = timezone.now()
    upcoming_tenders = tenders.filter(opening_date__gt=now, status='published').count()
    closing_soon = tenders.filter(closing_date__gt=now, closing_date__lte=now + timezone.timedelta(days=7), status='published').count()
    
    context = {
        'tenders': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'total_count': total_tenders,
        'draft_count': draft_count,
        'published_count': published_count,
        'closed_count': closed_count,
        'awarded_count': awarded_count,
        'upcoming_tenders': upcoming_tenders,
        'closing_soon': closing_soon,
    }
    return render(request, 'tender/list.html', context)


@login_required
def tender_detail(request, pk):
    """View tender details."""
    tender = get_object_or_404(Tender, pk=pk)
    
    # Check tender status
    now = timezone.now()
    is_upcoming = tender.opening_date > now
    is_open = tender.opening_date <= now <= tender.closing_date and tender.status == 'published'
    is_closed = tender.closing_date < now or tender.status in ['closed', 'awarded']
    
    context = {
        'tender': tender,
        'is_upcoming': is_upcoming,
        'is_open': is_open,
        'is_closed': is_closed,
        'now': now,
    }
    return render(request, 'tender/detail.html', context)


@login_required
def tender_create(request):
    """Create a new tender."""
    if request.method == 'POST':
        form = TenderForm(request.POST)
        if form.is_valid():
            tender = form.save()
            messages.success(request, f'Tender {tender.tender_number} created successfully!')
            return redirect('tender:detail', pk=tender.pk)
    else:
        form = TenderForm()
    
    context = {
        'form': form,
        'title': 'Add New Tender',
    }
    return render(request, 'tender/form.html', context)


@login_required
def tender_update(request, pk):
    """Update an existing tender."""
    tender = get_object_or_404(Tender, pk=pk)
    
    if request.method == 'POST':
        form = TenderForm(request.POST, instance=tender)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tender {tender.tender_number} updated successfully!')
            return redirect('tender:detail', pk=tender.pk)
    else:
        form = TenderForm(instance=tender)
    
    context = {
        'form': form,
        'tender': tender,
        'title': 'Update Tender',
    }
    return render(request, 'tender/form.html', context)


@login_required
def tender_delete(request, pk):
    """Delete a tender."""
    tender = get_object_or_404(Tender, pk=pk)
    
    if request.method == 'POST':
        tender_number = tender.tender_number
        tender.delete()
        messages.success(request, f'Tender {tender_number} deleted successfully!')
        return redirect('tender:list')
    
    context = {
        'tender': tender,
    }
    return render(request, 'tender/delete.html', context)
