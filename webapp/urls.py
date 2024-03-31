"""
URL configuration for webapp project.

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
from django.urls import re_path
from web import apirest, views



urlpatterns = [
    path('admin', admin.site.urls),
    path('login', apirest.login),
    path('logout', apirest.logout),
    path('send_evidence', apirest.send_evidence),
    path('edit_evidence', apirest.edit_evidence),
    path('delete_evidence', apirest.revidence),
    path('add_evidence', apirest.subir_evidence),
    path('send_csv', apirest.send_csv),
    path('send_sactivities', apirest.send_sactivities),
    path('send_type', apirest.send_type),
    path('send_rol', apirest.send_rol),
    path('send_activities', apirest.send_activities),
    path('send_users', apirest.send_users),
    path('delete_username', apirest.rusers),
    path('add_username', apirest.add_users),
    path('edit_user', apirest.edit_users),
    path('subir_sactivities', apirest.subir_sactivities),
    path('edit_sactivities', apirest.edit_sactivities),
    path('add_sactivities', apirest.add_sactivities),
    path('ractivities', apirest.ractivities),
    path('asistencia', apirest.send_asistencia),
    path('', views.handler),
    re_path(r'^(?P<path>.*)$', views.handler),
] 