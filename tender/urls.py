from django.urls import path
from . import views

app_name = 'tender'

urlpatterns = [
    path('', views.tender_list, name='list'),
    path('create/', views.tender_create, name='create'),
    path('<int:pk>/', views.tender_detail, name='detail'),
    path('<int:pk>/update/', views.tender_update, name='update'),
    path('<int:pk>/delete/', views.tender_delete, name='delete'),
]
