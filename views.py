from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .forms import *


@login_required(login_url='login')

def streamlit_view(request):
    user=request.user
    T_forms=TocsForms()
    A_forms=AddressForms()
    if request.method == 'POST':
        T_forms=TocsForms(request.POST)
        if forms.is_valid():
            # tocs = Tocs.objects.create(
            #     user=user, )
            # tocs.save()
            pass
    return render(request, 'base/index.html', {'T_forms':T_forms})

def login(request):
    error_message = None

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            error_message = "Please fill all the fields"
        else:
            user = authenticate(request, username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('index')
            else:
                error_message = "Username or password incorrect"

    return render(request, 'base/login.html', {'erreur': error_message})
def logoutPage(request):
    logout(request)
    return redirect('login')


