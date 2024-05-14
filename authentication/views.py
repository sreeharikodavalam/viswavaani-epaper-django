from django.shortcuts import redirect, render
from django.contrib.auth import authenticate,login as core_login
from django.urls import reverse


# Create your views here.

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
