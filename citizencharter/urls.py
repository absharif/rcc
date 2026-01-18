from django.urls import path
from . import views

app_name = 'citizencharter'

urlpatterns = [
    path('', views.citizencharter_list, name='list'),
    path('create/', views.citizencharter_create, name='create'),
    path('<int:pk>/', views.citizencharter_detail, name='detail'),
    path('<int:pk>/update/', views.citizencharter_update, name='update'),
    path('<int:pk>/delete/', views.citizencharter_delete, name='delete'),
]
