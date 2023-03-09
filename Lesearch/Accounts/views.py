from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.template import loader
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
#ユーザの詳細情報取得用に追加
from django.shortcuts import get_object_or_404
from Accounts.models import UserInfo

from .forms import SignupForm, LoginForm, UserForm
from .models import Profile
# Create your views here.


def signup_view(request):
    if request.method == 'POST':

        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()

    else:
        form = SignupForm()
    
    param = {
        'form': form
    }

    return render(request, 'login_app/signup.html', param)

def login_view(request):
    print(request.method)
    
    # POSTでアクセスがあった場合
    if request.method == 'POST':
        print(request.method)
        next = request.POST.get('next')
        print(next)
        form = LoginForm(request, data=request.POST)
        print(form)

        if form.is_valid():
            user = form.get_user()
            print(user)
            #if user:
                #login(request, user)
                #return redirect(to='/login_app/user/')

            
            if user:
                login(request, user)
                if next == 'None':
                    return redirect(to="user")


                else:
                    return redirect(to=next)
            
    
    # GETでアクセスがあった場合
    else:
        form = LoginForm()
        next = request.GET.get('next')
    
    
    param = {
        'form': form,
        'next': next
    }

    return render(request, 'login_app/login.html', param)


@login_required
def logout_view(request):
    logout(request)


    return render(request, 'login_app/logout.html')

@login_required
def user_view(request):
    user = request.user
    print(user.username)
    clientsinfo = UserInfo.objects.all()
    consultantName = user.username
    clientName1 = "クライアントが登録されていません"
    clientName2 = "クライアントが登録されていません"
    clientName3 = "クライアントが登録されていません"

    for clientinfo in clientsinfo:
        #print(clientinfo.consultantName)
        if clientinfo.consultantName == user.username :
            consultantName = clientinfo.consultantName
            clientName1 = clientinfo.clientName1
            clientName2 = clientinfo.clientName2
            clientName3 = clientinfo.clientName3 
    print(consultantName)
    print(clientName1)
    print(clientName2)
    print(clientName3)


    #フォームを変数にセット
    form = UserForm()

    context = {
        'userForm':form,
        'user': user ,
        'consultantName': consultantName ,
        'clientName1': clientName1 ,
        'clientName2': clientName2 ,
        'clientName3': clientName3 ,
    }


    return render(request, 'login_app/user.html', context=context)




# フォームから受取ったデータをDBに登録する
@login_required
def addUser(request):
    #リクエストがPOSTの場合
    if request.method == 'POST':
        #リクエストをもとにフォームをインスタンス化
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            userForm.save()
 
    #登録後、全件データを抽出
    userinfo = UserInfo.objects.all()
    context = {
        'msg': '現在の利用状況',
        'userinfo': userinfo,
        'count':userinfo.count,
    }
 
    #user.htmlへデータを渡す
    return render(request, 'login_app/users.html',context)




@login_required
def follow(request, user_id):
    user = User.objects.get(id=user_id)
    request.user.profile.followings.add(user)
    return redirect('login_app/user_detail', user_id=user_id)

@login_required
def unfollow(request, user_id):
    user = User.objects.get(id=user_id)
    request.user.profile.followings.remove(user)
    return redirect('login_app/user_detail', user_id=user_id)





"""
@login_required
def other_view(request):
    users = User.objects.exclude(username=request.user.username)

    params = {
        'users': users
    }

    return render(request, 'login_app/other.html', params)
"""

@login_required
def showCreateClientForm(request):
    #フォームを変数にセット
    form = UserForm()
 
    context = {
        'userForm':form,
    }
 
    #detail.htmlへデータを渡す
    return render(request, 'login_app/create.html',context)
