from django.shortcuts import render
from django.db.models import query
from django.shortcuts import redirect, render
from django.http.response import HttpResponse
from django.views.generic import View
from django.contrib.sites.shortcuts import get_current_site
from .models import User_info

def login_view(request):

  if 'user_email' in request.session:
    return redirect('home')

  return render(request, 'login.html')

def logout(request):
  del request.session['user_email']
  return redirect('login_view')


def join_view(request):
  return render(request, 'join.html')

def login_action(request):
  email = request.POST.get('email')
  raw_pw = request.POST.get('raw_pw')
  queryset = User_info.objects.filter(user_email = email, user_pwd = raw_pw)
  
  if len(queryset) == 1 :
    request.session['user_email'] = email
    return redirect('home')

  return render(request, 'login.html',{'message':True})


def join_action(request):
  data = request.POST
  User_info.objects.create(user_email=data.get('user_email', False), user_pwd=data.get('user_pwd'), user_name=data.get('user_name', False))
  return redirect('login_view')


def join_email_overap(request):
  email = request.GET['email']
  queryset = User_info.objects.filter(user_email = email)
  if len(queryset) > 0:
    return HttpResponse('Overap')
  return HttpResponse('Usable')

def is_sess_attached(request):  # 현재 로그인 한 user면 is_sess = True
  is_sess = False
  if 'user_email' in request.session:
    is_sess = True
  return is_sess

def get_user_inst(request):      # 나중에 해당 user가 그 user가 맞는지 확인하여 그  user 정보 한 줄을 디비에서 빼와주는 함수.
  if is_sess_attached(request):
    email = request.session['user_email']
    queryset = User_info.objects.filter(user_email = email)
    return queryset[0]


def is_login(request):
  if 'user_email' in request.session:
    return HttpResponse('true')
  return HttpResponse('false')