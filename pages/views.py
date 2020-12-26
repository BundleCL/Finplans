from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .forms import SignUpForm
from .forms import FinancialDataForm


def index(request):
    # return HttpResponse('<h1>Hello finplans</h1>')
    return render(request, 'index.html')


def register(request):
    form = SignUpForm()

    print(form.errors)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if (form.is_valid()):
            # form.save()
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
                #return redirect("https://docs.google.com/forms/d/e/1FAIpQLSfTVN6PxiaZkTKmPmZdFL86Hb_Tril-_pEBtM2gV5SePkKRMg/viewform?usp=sf_link")
                return redirect('index')
            except Exception as e:
                print(e)
    return render(request, 'register.html', {'form': form})

def profile(request):
    form = FinancialDataForm()

    if request.method == 'POST':
        form = FinancialDataForm(request.POST)
    return render(request, 'profile.html', {'form': form})