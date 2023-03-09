from django.urls import path
from . import views

urlpatterns = [
    path('friends/', views.friends, name='friends'),
    path('platforms/', views.platforms, name='platforms'),
    path('customers/', views.customers, name='customers'),
    path('surveys/', views.surveys, name='surveys'),
    path('menus/', views.menus, name='menus'),
    path('channels/', views.channels, name='channels'),
    path('conversions/', views.conversions, name='conversions'),
    path('test/', views.test, name='test'),
]