from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login as django_login
from django.contrib.auth.decorators import login_required
# Create your views here.
def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username == '' or password == '':
            messages.error('Please fill all fields')
            return redirect('login')
        if not (User.objects.filter(username=username).exists()):
            messages.error(request,'User does not exist')
            return redirect('login')
        user=authenticate(username=username,password=password)
        if user == None :
            messages.error(request,'Invalid password')
            return redirect('login')
        else:
            django_login(request,user)
            messages.success(request,'Logged in successfully')
            return redirect('home')
    template=loader.get_template('login.html')
    context = {}
    return HttpResponse(template.render(context,request))

def signup(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        if username == '' or password == '':
            messages.error('Please fill all fields')
            return redirect('signup')
        if User.objects.filter(username=username).exists():
            messages.error(request,'User already exists')
            return redirect('signup')
        user=User.objects.create_user(username=username)
        user.set_password(password)
        user.save()
        messages.success(request,'Signed Up successfully')
        return redirect('login')
    template=loader.get_template('signup.html')
    context = {}
    return HttpResponse(template.render(context,request))
@login_required
def home(request):
    return HttpResponse('Welcome to the home page')