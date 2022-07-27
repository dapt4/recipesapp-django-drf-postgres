from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login),
    path('register', views.register),
    path("doctor", views.doctor),
    path("doctor/<int:id>", views.edit_doctor),
    path("drug", views.drug),
    path("recipe", views.recipe),
    path("recipe/<int:id>", views.edit_recipe),
]
