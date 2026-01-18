from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Citizen, CitizenDocument
from .forms import CitizenForm, CitizenDocumentForm


@login_required
def citizen_list(request):
    """List all citizens with search and pagination."""
    citizens = Citizen.objects.filter(is_active=True)
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        citizens = citizens.filter(
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(national_id__icontains=search_query) |
            Q(phone_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(citizens, 20)  # Show 20 citizens per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'citizens': page_obj,
        'search_query': search_query,
        'total_count': citizens.count(),
    }
    return render(request, 'citizen/list.html', context)


@login_required
def citizen_detail(request, pk):
    """View citizen details."""
    citizen = get_object_or_404(Citizen, pk=pk)
    documents = citizen.documents.all()
    
    context = {
        'citizen': citizen,
        'documents': documents,
    }
    return render(request, 'citizen/detail.html', context)


@login_required
def citizen_create(request):
    """Create a new citizen."""
    if request.method == 'POST':
        form = CitizenForm(request.POST, request.FILES)
        if form.is_valid():
            citizen = form.save(commit=False)
            citizen.created_by = request.user
            citizen.save()
            messages.success(request, f'Citizen {citizen.full_name} created successfully!')
            return redirect('citizen:detail', pk=citizen.pk)
    else:
        form = CitizenForm()
    
    context = {
        'form': form,
        'title': 'Add New Citizen',
    }
    return render(request, 'citizen/form.html', context)


@login_required
def citizen_update(request, pk):
    """Update an existing citizen."""
    citizen = get_object_or_404(Citizen, pk=pk)
    
    if request.method == 'POST':
        form = CitizenForm(request.POST, request.FILES, instance=citizen)
        if form.is_valid():
            form.save()
            messages.success(request, f'Citizen {citizen.full_name} updated successfully!')
            return redirect('citizen:detail', pk=citizen.pk)
    else:
        form = CitizenForm(instance=citizen)
    
    context = {
        'form': form,
        'citizen': citizen,
        'title': 'Update Citizen',
    }
    return render(request, 'citizen/form.html', context)


@login_required
def citizen_delete(request, pk):
    """Delete a citizen (soft delete by setting is_active=False)."""
    citizen = get_object_or_404(Citizen, pk=pk)
    
    if request.method == 'POST':
        citizen.is_active = False
        citizen.save()
        messages.success(request, f'Citizen {citizen.full_name} deleted successfully!')
        return redirect('citizen:list')
    
    context = {
        'citizen': citizen,
    }
    return render(request, 'citizen/delete.html', context)


@login_required
def citizen_document_add(request, citizen_pk):
    """Add a document to a citizen."""
    citizen = get_object_or_404(Citizen, pk=citizen_pk)
    
    if request.method == 'POST':
        form = CitizenDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.citizen = citizen
            document.save()
            messages.success(request, 'Document added successfully!')
            return redirect('citizen:detail', pk=citizen.pk)
    else:
        form = CitizenDocumentForm()
    
    context = {
        'form': form,
        'citizen': citizen,
        'title': 'Add Document',
    }
    return render(request, 'citizen/document_form.html', context)


@login_required
def citizen_document_delete(request, pk):
    """Delete a citizen document."""
    document = get_object_or_404(CitizenDocument, pk=pk)
    citizen_pk = document.citizen.pk
    
    if request.method == 'POST':
        document.delete()
        messages.success(request, 'Document deleted successfully!')
        return redirect('citizen:detail', pk=citizen_pk)
    
    context = {
        'document': document,
    }
    return render(request, 'citizen/document_delete.html', context)
