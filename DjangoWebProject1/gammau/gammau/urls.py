"""
Definition of urls for gammau.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.urls import path
from app import views

urlpatterns = [
    path('', views.main, name='main')
,path("creds/",views.creds,name="creds"),
path("exec/",views.execute_script,name="execute_script"),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),
]
