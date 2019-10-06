from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='starboardscanner_app-home'),
]
