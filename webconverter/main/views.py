from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
def index(request):
    if request.user.is_authenticated:
        print(request.user.password)
    return render(request, 'index.html')


@login_required(login_url='/')
def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)

@login_required(login_url='/')
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        u = User.objects.get(username=request.user.username)
        u.set_password(password)
        u.save()
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            authenticate(username=request.user.username, password=password)
            print("logged in")
            return redirect('profile')
        else:
            print("!!!User does not exist")
            return redirect('/')
    else:
        return redirect('/')


def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        duplicate, duplicate_email = False, False
        try:
            duplicate = User.objects.get(username=username)
        except: pass
        try:
            duplicate_email = User.objects.get(email=email)
        except: pass
        if duplicate or duplicate_email:
            messages.error(request, 'Такой аккаунт уже зарегистрирован! Войдите в аккаунт.')
            return redirect('/')
        else:
            user = User()
            user.email = email
            user.username = username
            user.password = make_password(password)
            user.save()
            user = authenticate(email=email, username=username, password=password)
            login(request, user, backend=None)
            messages.success(request, 'Вы успешно создали аккаунт!')
            return redirect('/')



def login_user(request):
    if request.method == 'POST':
        login_str = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(email=login_str, password=password)
        if user is None:
            user = authenticate(username=login_str, password=password)
        if user is not None:
            messages.success(request, 'Вы успешно вошли в свой аккаунт')
            login(request, user, backend=None)
            return redirect('/')
        else:
            messages.error(request, 'Введите корректные данные')
            return redirect('/')

