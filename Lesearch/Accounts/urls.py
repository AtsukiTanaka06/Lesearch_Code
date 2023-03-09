from django.urls import path
from .import views

from django.contrib.auth import views as auth_views
from django.urls import path
from .views import follow, unfollow


urlpatterns = [
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    #path('login', auth_views.LoginView.as_view(template_name='login_app/login.html')),
    path('logout', views.logout_view, name='logout'),
    path('user', views.user_view, name='user'),
    #path('other', views.other_view, name='other'),
    #ユーザの登録フォームを呼び出す
    path('create', views.showCreateClientForm, name='showCreateClientForm'),
     #ユーザ登録する処理を呼び出す
    path('add', views.addUser, name='addUser'),

    path('follow/<int:user_id>/', follow, name='follow'),
    path('unfollow/<int:user_id>/', unfollow, name='unfollow'),

]



