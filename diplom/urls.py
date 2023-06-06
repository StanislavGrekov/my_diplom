"""
URL configuration for diplom project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from orders.views import  product_info
from orders.forms import login, registration_contact, registration

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/login', login, name='login'),
    path('user/registration', registration, name='registration'),
    path('user/registration/contact', registration_contact, name='registration_contact'),
    path('user/product_info', product_info, name='product_info'),


]