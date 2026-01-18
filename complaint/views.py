from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.utils import timezone
from .models import Complaint
from .forms import ComplaintForm


@login_required
def complaint_list(request):
    """List all complaints with search and pagination."""
    complaints = Complaint.objects.select_related('citizen').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    
    if search_query:
        complaints = complaints.filter(
            Q(complaint_number__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(citizen__first_name__icontains=search_query) |
            Q(citizen__last_name__icontains=search_query) |
            Q(citizen__national_id__icontains=search_query)
        )
    
    if status_filter:
        complaints = complaints.filter(status=status_filter)
    
    if priority_filter:
        complaints = complaints.filter(priority=priority_filter)
    
    # Pagination
    paginator = Paginator(complaints, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    total_complaints = complaints.count()
    submitted_count = complaints.filter(status='submitted').count()
    in_progress_count = complaints.filter(status='in_progress').count()
    resolved_count = complaints.filter(status='resolved').count()
    closed_count = complaints.filter(status='closed').count()
    urgent_count = complaints.filter(priority='urgent').count()
    
    context = {
        'complaints': page_obj,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'total_count': total_complaints,
        'submitted_count': submitted_count,
        'in_progress_count': in_progress_count,
        'resolved_count': resolved_count,
        'closed_count': closed_count,
        'urgent_count': urgent_count,
    }
    return render(request, 'complaint/list.html', context)


@login_required
def complaint_detail(request, pk):
    """View complaint details."""
    complaint = get_object_or_404(Complaint.objects.select_related('citizen'), pk=pk)
    
    context = {
        'complaint': complaint,
    }
    return render(request, 'complaint/detail.html', context)


@login_required
def complaint_create(request):
    """Create a new complaint."""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save()
            messages.success(request, f'Complaint {complaint.complaint_number} created successfully!')
            return redirect('complaint:detail', pk=complaint.pk)
    else:
        form = ComplaintForm()
    
    context = {
        'form': form,
        'title': 'Add New Complaint',
    }
    return render(request, 'complaint/form.html', context)


@login_required
def complaint_update(request, pk):
    """Update an existing complaint."""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        form = ComplaintForm(request.POST, instance=complaint)
        if form.is_valid():
            # Set resolved_at if status changed to resolved
            if form.cleaned_data['status'] == 'resolved' and not complaint.resolved_at:
                complaint.resolved_at = timezone.now()
            elif form.cleaned_data['status'] != 'resolved':
                complaint.resolved_at = None
            form.save()
            messages.success(request, f'Complaint {complaint.complaint_number} updated successfully!')
            return redirect('complaint:detail', pk=complaint.pk)
    else:
        form = ComplaintForm(instance=complaint)
    
    context = {
        'form': form,
        'complaint': complaint,
        'title': 'Update Complaint',
    }
    return render(request, 'complaint/form.html', context)


@login_required
def complaint_delete(request, pk):
    """Delete a complaint."""
    complaint = get_object_or_404(Complaint, pk=pk)
    
    if request.method == 'POST':
        complaint_number = complaint.complaint_number
        complaint.delete()
        messages.success(request, f'Complaint {complaint_number} deleted successfully!')
        return redirect('complaint:list')
    
    context = {
        'complaint': complaint,
    }
    return render(request, 'complaint/delete.html', context)
