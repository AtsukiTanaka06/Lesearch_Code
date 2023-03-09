from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('top', views.top, name='top'),
    path('top1/<str:key>', views.top1, name='top1'),
    
]