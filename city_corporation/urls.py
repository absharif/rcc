"""
URL configuration for city_corporation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views

# Customize admin site
admin.site.site_header = "City Corporation Administration"
admin.site.site_title = "City Corporation Admin"
admin.site.index_title = "Welcome to City Corporation Management System"

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.dashboard, name='dashboard'),
    path('admin/dashboard/stats/', views.dashboard_stats_api, name='dashboard_stats'),
    path('admin/logout/', views.logout_view, name='logout'),
    path('django-admin/', admin.site.urls),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
