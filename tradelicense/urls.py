from django.urls import path
from . import views

app_name = 'tradelicense'

urlpatterns = [
    path('', views.trade_license_list, name='list'),
    path('create/', views.trade_license_create, name='create'),
    path('<int:pk>/', views.trade_license_detail, name='detail'),
    path('<int:pk>/update/', views.trade_license_update, name='update'),
    path('<int:pk>/delete/', views.trade_license_delete, name='delete'),
]
