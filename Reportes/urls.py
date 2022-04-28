"""Reportes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app_seguridad import views
from django.conf.urls.static import static

urlpatterns = [
    # Url para el admin
    path('admin/', admin.site.urls),

    #Urls para el inicio de sesion
    path('', views.page_login, name='page_login'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),

    # Urls para la app de reportes de levanter
    path('Reportes/', include('app_reportes.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
