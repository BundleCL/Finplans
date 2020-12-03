from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User


def index(request):
    # return HttpResponse('<h1>Hello finplans</h1>')
    return render(request, 'index.html')


def register(request):
    form = SignUpForm()

    print(form.errors)
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            user = User.objects.create_user(
                username=email, email=email, password=password, first_name=first_name, last_name=last_name)
            return redirect('index')
    return render(request, 'register.html', {'form': form})
