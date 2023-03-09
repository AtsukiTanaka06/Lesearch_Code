from django.urls import path
from . import views

urlpatterns = [
    path('columns/', views.columns, name='columns'),
]