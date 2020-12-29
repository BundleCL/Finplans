from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .forms import FinancialDataForm
from .models import Financial, Option
from .optimize import solve


def index(request):
    return render(request, 'index.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('survey')
    form = SignUpForm()
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if (form.is_valid()):
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            try:
                form.check_mail(email)
                user = User.objects.create_user(username=email, email=email, password=password,
                first_name=first_name, last_name=last_name)
                send_mail(
                    'Nuevo usuario',
                    f'Se ha registrado {user.first_name} {user.last_name}, {user.email} en Finplans',
                    'contacto.finplans@gmail.com',
                    ['contacto.finplans@gmail.com'],
                    fail_silently=False,
                )
                if user is not None:
                    do_login(request, user)
                    return redirect('survey')
                #return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfTVN6PxiaZkTKmPmZdFL86Hb_Tril-_pEBtM2gV5SePkKRMg/viewform?usp=sf_link")
                return redirect('index')
            except Exception as e:
                print(e)
    return render(request, 'register.html', {'form': form})

@login_required(login_url='login')
def survey(request):
    form = FinancialDataForm()
    if request.method == 'POST':
        form = FinancialDataForm(request.POST)
        if (form.is_valid()):
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('index') #profile --pending

    return render(request, 'survey.html', {'form': form})

@login_required(login_url='login')
def profile(request):
    if not request.user.financial_set.first():
        return redirect('survey')
    #filtrar usuario para ver datos ingresados
    # reemplazar datos desde solver
    res_1 = {}
    res_2 = {}
    res_3 = {}
    return render(request, "profile.html", {'res_1': res_1, 'res_2': res_2, 'res_3': res_3})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                return redirect('survey')

    return render(request, "login.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('index')