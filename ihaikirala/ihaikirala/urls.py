"""
URL configuration for ihaikirala project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from ihakiralama import views
from django.urls import path, include
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'iha', views.İHAViewSet)
router.register(r'kiralanan', views.KiralananViewSet)


urlpatterns = [
    path('', views.login_view, name='anasayfa'),
    path('admin/', admin.site.urls),
    path('anasayfa', views.anasayfa_view, name='anasayfa'),  # Anasayfa URL deseni
    path('login/', views.login_view, name='login'),  
    path('register', views.register_view, name='register'),
    path('iha_ekle', views.iha_ekle_view, name='iha_ekle'),
    path('iha_kirala', views.iha_kirala_view, name='iha_kirala'),
    path('iha_listele', views.iha_listele_view, name='iha_listele'),
    path('iha_guncelle/<int:iha_id>', views.iha_guncelle_view, name='iha_guncelle'),
    path('kiralanan_ihalar', views.kiralanan_ihalar_listele_view, name='kiralanan_ihalar_listele'),
    path('kiralanan_iha_guncelle/<int:kiralanan_id>', views.kiralanan_iha_guncelle_view, name='kiralanan_iha_guncelle'),

    path('api/', include(router.urls)),

]
