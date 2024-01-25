"""
URL configuration for PO_projekt project.

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
from django.urls import path, include

import biblioteka_app
from biblioteka_app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/', include('biblioteka_app.urls'), name="api"),
    path('rent_online/<int:book_id>/', views.rent_online, name='rent_online'),
    path('make_reservation/<int:book_id>/', views.make_reservation, name='make_reservation'),
]
