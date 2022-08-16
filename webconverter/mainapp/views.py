from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
@login_required(login_url='login_user')
def index(request):
    if request.user.is_authenticated:
        print(request.user.password)
    return render(request, 'index.html')


@login_required(login_url='login_user')
def profile(request):
    context = {
        'user': request.user
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login_user')
def change_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        u = User.objects.get(username=request.user.username)
        u.set_password(password)
        u.save()
        user = authenticate(username=request.user.username, password=password)
        if user is not None:
            authenticate(username=request.user.username, password=password)
            messages.success(request, 'Пароль изменен!')
            return redirect('profile')
        else:
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
    else:
        return render(request, 'register.html')


def login_user(request):
    if request.method == 'POST':
        login_str = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(username=login_str, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Вы успешно вошли в аккаунт')
            return redirect('/')
        else:
            messages.error(request, 'Введите корректные данные')
            return redirect('/')
    else:
        return render(request, 'login.html')
