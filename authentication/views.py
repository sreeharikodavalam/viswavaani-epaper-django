from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login as core_login
from django.urls import reverse
from django.contrib.auth.views import auth_logout

def login(request):
    login_failed = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                core_login(request, user)
                return redirect(reverse('epaper-home'))
        login_failed = True
    return render(request, 'authentication/login.html', {'login_failed': login_failed})


def logout(request):
    auth_logout(request)
    redirect(reverse('login'))
    return render(request, 'authentication/login.html', {'login_failed': False})
