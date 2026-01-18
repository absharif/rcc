from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import CitizenCharter
from .forms import CitizenCharterForm


@login_required
def citizencharter_list(request):
    """List all citizen charters with search and pagination."""
    charters = CitizenCharter.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    service_filter = request.GET.get('service_type', '')
    active_filter = request.GET.get('active', '')
    
    if search_query:
        charters = charters.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(required_documents__icontains=search_query)
        )
    
    if service_filter:
        charters = charters.filter(service_type=service_filter)
    
    if active_filter == 'true':
        charters = charters.filter(is_active=True)
    elif active_filter == 'false':
        charters = charters.filter(is_active=False)
    
    # Pagination
    paginator = Paginator(charters, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_charters = charters.count()
    active_count = charters.filter(is_active=True).count()
    inactive_count = charters.filter(is_active=False).count()
    
    # Count by service type
    service_counts = charters.values('service_type').annotate(count=Count('id'))
    
    context = {
        'charters': page_obj,
        'search_query': search_query,
        'service_filter': service_filter,
        'active_filter': active_filter,
        'total_count': total_charters,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'service_counts': service_counts,
    }
    return render(request, 'citizencharter/list.html', context)


@login_required
def citizencharter_detail(request, pk):
    """View citizen charter details."""
    charter = get_object_or_404(CitizenCharter, pk=pk)
    
    context = {
        'charter': charter,
    }
    return render(request, 'citizencharter/detail.html', context)


@login_required
def citizencharter_create(request):
    """Create a new citizen charter."""
    if request.method == 'POST':
        form = CitizenCharterForm(request.POST)
        if form.is_valid():
            charter = form.save()
            messages.success(request, f'Citizen Charter "{charter.title}" created successfully!')
            return redirect('citizencharter:detail', pk=charter.pk)
    else:
        form = CitizenCharterForm()
    
    context = {
        'form': form,
        'title': 'Add New Citizen Charter',
    }
    return render(request, 'citizencharter/form.html', context)


@login_required
def citizencharter_update(request, pk):
    """Update an existing citizen charter."""
    charter = get_object_or_404(CitizenCharter, pk=pk)
    
    if request.method == 'POST':
        form = CitizenCharterForm(request.POST, instance=charter)
        if form.is_valid():
            form.save()
            messages.success(request, f'Citizen Charter "{charter.title}" updated successfully!')
            return redirect('citizencharter:detail', pk=charter.pk)
    else:
        form = CitizenCharterForm(instance=charter)
    
    context = {
        'form': form,
        'charter': charter,
        'title': 'Update Citizen Charter',
    }
    return render(request, 'citizencharter/form.html', context)


@login_required
def citizencharter_delete(request, pk):
    """Delete a citizen charter."""
    charter = get_object_or_404(CitizenCharter, pk=pk)
    
    if request.method == 'POST':
        title = charter.title
        charter.delete()
        messages.success(request, f'Citizen Charter "{title}" deleted successfully!')
        return redirect('citizencharter:list')
    
    context = {
        'charter': charter,
    }
    return render(request, 'citizencharter/delete.html', context)
