from django.urls import path
from . import views
from . import views_citizen

app_name = 'citizen'

urlpatterns = [
    # Admin routes (for admin users)
    path('', views.citizen_list, name='list'),
    path('create/', views.citizen_create, name='create'),
    path('<int:pk>/', views.citizen_detail, name='detail'),
    path('<int:pk>/update/', views.citizen_update, name='update'),
    path('<int:pk>/delete/', views.citizen_delete, name='delete'),
    path('<int:citizen_pk>/document/add/', views.citizen_document_add, name='document_add'),
    path('document/<int:pk>/delete/', views.citizen_document_delete, name='document_delete'),
    
    # Citizen routes (for citizen users)
    path('dashboard/', views_citizen.citizen_dashboard, name='citizen_dashboard'),
    path('my-properties/', views_citizen.citizen_properties, name='citizen_properties'),
    path('my-taxes/', views_citizen.citizen_holding_taxes, name='citizen_holding_taxes'),
    path('my-licenses/', views_citizen.citizen_trade_licenses, name='citizen_trade_licenses'),
    path('my-certifications/', views_citizen.citizen_certifications, name='citizen_certifications'),
]
