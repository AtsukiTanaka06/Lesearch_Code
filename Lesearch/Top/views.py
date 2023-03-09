# Djangoモジュール
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required

from .models import UserSettings
from .form import UploadCSVForm

import sys
sys.path.append("../")
from Pythons import handle_uploaded_file

# ホームページView
def home(request):
    template = loader.get_template('home.html')
    context = {'name': 'ホームページ'}

    return HttpResponse(template.render(context, request))

# トップページView
def top(request):
    template = loader.get_template('top.html')
    context = {'name': 'トップページ'}

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            context['file'] = file
            handle_uploaded_file(file)
            status = True
    else:
        form = UploadCSVForm()
        status = False

    context['form'] = form
    context['file_status'] = status

    return HttpResponse(template.render(context, request))

# トップページView
@login_required
def top1(request,key):
    template = loader.get_template('top1.html')
    context = {'name': 'トップページ'}
    print(key)

    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            context['file'] = file
            handle_uploaded_file(file)
            status = True
    else:
        form = UploadCSVForm()
        status = False

    context['form'] = form
    context['file_status'] = status
    context['clientName'] = key

    return HttpResponse(template.render(context, request))