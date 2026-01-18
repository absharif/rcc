"""
Custom decorators for role-based access control.
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def group_required(*group_names):
    """
    Decorator to check if user belongs to any of the specified groups.
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.is_superuser:
                return view_func(request, *args, **kwargs)
            
            user_groups = request.user.groups.values_list('name', flat=True)
            if any(group_name in user_groups for group_name in group_names):
                return view_func(request, *args, **kwargs)
            
            messages.error(request, 'You do not have permission to access this page.')
            return redirect('home')
        return wrapper
    return decorator


def superadmin_required(view_func):
    """
    Decorator to check if user is superadmin (has Django admin access).
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser or request.user.groups.filter(name='SuperAdmin').exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return wrapper


def citizen_required(view_func):
    """
    Decorator to check if user is a citizen.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if request.user.groups.filter(name='citizen').exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return wrapper


def field_officer_required(view_func):
    """
    Decorator to check if user is a Holding Tax Field Officer.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if request.user.groups.filter(name='Holding Tax Field Officer').exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return wrapper


def officer_required(view_func):
    """
    Decorator to check if user is an Officer.
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        if request.user.groups.filter(name='Officer').exists():
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('home')
    return wrapper
