"""GoldDigger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from GDapp import views, ajax_views
from django.conf.urls.static import static
from django.conf import settings
from rest_framework.routers import DefaultRouter

ajax_router = DefaultRouter()
ajax_router.register(r'', ajax_views.RelatedImageAJAXView)
 #not registering the mask here yet for simplicity

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('image_upload/', views.image_view, name='image_upload'),
    path('run_gd/<int:pk>', views.run_gd, name='run_gd'),
    url(r'related_images/', include(ajax_router.urls)),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# for development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
