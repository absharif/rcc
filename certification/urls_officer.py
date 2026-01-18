"""
URLs for Officer role.
"""
from django.urls import path
from . import views_officer

app_name = 'officer'

urlpatterns = [
    path('dashboard/', views_officer.officer_dashboard, name='dashboard'),
    path('holding-taxes/', views_officer.officer_holdingtax_list, name='holdingtax_list'),
    path('holding-taxes/<int:pk>/approve/', views_officer.officer_holdingtax_approve, name='holdingtax_approve'),
    path('certifications/', views_officer.officer_certification_list, name='certification_list'),
    path('certifications/<int:pk>/approve/', views_officer.officer_certification_approve, name='certification_approve'),
]
