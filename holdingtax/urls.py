from django.urls import path
from . import views

app_name = 'holdingtax'

urlpatterns = [
    # Holding Tax URLs
    path('', views.holding_tax_list, name='list'),
    path('create/', views.holding_tax_create, name='create'),
    path('<int:pk>/', views.holding_tax_detail, name='detail'),
    path('<int:pk>/update/', views.holding_tax_update, name='update'),
    path('<int:pk>/delete/', views.holding_tax_delete, name='delete'),
    path('<int:holding_tax_pk>/payment/add/', views.tax_payment_add, name='payment_add'),
    
    # Property URLs
    path('properties/', views.property_list, name='property_list'),
    path('properties/create/', views.property_create, name='property_create'),
    path('properties/<int:pk>/', views.property_detail, name='property_detail'),
    path('properties/<int:pk>/update/', views.property_update, name='property_update'),
]
