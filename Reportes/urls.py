from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from app_seguridad import views
from django.conf.urls.static import static

urlpatterns = [
    # Url para pagina de administración
    path('admin/', admin.site.urls),

    #Urls para el inicio de sesion
    path('', views.page_login, name='page_login'),
    path('login/', views.log_in, name='log_in'),
    path('logout/', views.log_out, name='log_out'),

    # Urls para la app de reportes de levanter
    path('Reportes/', include('app_reportes.urls')),
    path('Registro/', include('app_registro.urls')),
    
    # Agregar los archivos estático para ser usado en todas las Urls
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
