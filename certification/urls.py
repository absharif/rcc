from django.urls import path
from . import views

app_name = 'certification'

urlpatterns = [
    path('', views.certification_list, name='list'),
    path('create/', views.certification_create, name='create'),
    path('<int:pk>/', views.certification_detail, name='detail'),
    path('<int:pk>/update/', views.certification_update, name='update'),
    path('<int:pk>/delete/', views.certification_delete, name='delete'),
    path('<int:pk>/generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('<int:pk>/approve/', views.approve_certification, name='approve'),
]
