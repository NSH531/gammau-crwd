"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views


from django.db import models

def parse_json(DATA):
    class_dict = {}
    parse_json_recursive(class_dict, "Root", DATA)
    return class_dict

def parse_json_recursive(class_dict, class_name, data):
    if isinstance(data, dict):
        model_attrs = {}

        for attr_name, attr_value in data.items():
            if isinstance(attr_value, dict):
                nested_class_name = f"{class_name}_{attr_name}"
                nested_class_dict = {}
                parse_json_recursive(nested_class_dict, nested_class_name, attr_value)
                model_attrs[attr_name] = models.ForeignKey(nested_class_dict[nested_class_name], on_delete=models.CASCADE)
            else:
                model_attrs[attr_name] = convert_to_model_field(attr_value)

        new_class = type(class_name, (models.Model,), model_attrs)
        class_dict[class_name] = new_class

    elif isinstance(data, list):
        if data:
            # Assume all items in the list have the same structure
            parse_json_recursive(class_dict, class_name, data[0])

    else:
        # Non-dict types (e.g., string, number, boolean)
        class_dict[class_name] = convert_to_model_field(data)

def convert_to_model_field(value):
    if isinstance(value, str):
        return models.CharField(max_length=255)
    elif isinstance(value, int):
        return models.IntegerField()
    elif isinstance(value, float):
        return models.FloatField()
    elif isinstance(value, bool):
        return models.BooleanField()
    else:
        return models.CharField(max_length=255)

urlpatterns = [
    path('', views.main, name='main')
,path("creds/",views.creds,name="creds"),
path("exec/",views.execute_script,name="execute_script"),
    path('home/', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('admin/', admin.site.urls),

#    path('', views.home, name='home'),
]
print(parse_json(urlpatterns[0]))


