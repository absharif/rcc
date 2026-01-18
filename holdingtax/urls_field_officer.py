"""
URLs for Holding Tax Field Officer.
"""
from django.urls import path
from . import views_field_officer

app_name = 'field_officer'

urlpatterns = [
    path('dashboard/', views_field_officer.field_officer_dashboard, name='dashboard'),
    path('citizens/', views_field_officer.field_officer_citizen_list, name='citizen_list'),
    path('citizens/create/', views_field_officer.field_officer_citizen_create, name='citizen_create'),
    path('properties/', views_field_officer.field_officer_property_list, name='property_list'),
    path('properties/create/', views_field_officer.field_officer_property_create, name='property_create'),
    path('holding-taxes/', views_field_officer.field_officer_holdingtax_list, name='holdingtax_list'),
    path('holding-taxes/create/', views_field_officer.field_officer_holdingtax_create, name='holdingtax_create'),
]
