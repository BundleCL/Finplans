from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate
from django.contrib.auth import login as do_login
from django.contrib.auth import logout as do_logout
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
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
    financial_info = request.user.financial_set.first()
    if request.method == 'POST':
        form = FinancialDataForm(request.POST or None, instance=financial_info)
        if (form.is_valid()):
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            return redirect('results')
    else:
        if financial_info:
            form = FinancialDataForm(initial=model_to_dict(financial_info))
        else:
            form = FinancialDataForm()
    return render(request, 'survey.html', {'form': form})

@login_required(login_url='login')
def results(request):
    financial_info = request.user.financial_set.first()
    if not financial_info: # si no llena encuesta
        return redirect('survey')
    # reemplazar datos desde solver
    meta, plazo = financial_info.get_meta(), financial_info.get_plazo()
    DD, Gm, F = financial_info.get_DD(), financial_info.get_Gm(), financial_info.get_F()
    solver_data = solve(meta, plazo, DD, Gm, F)
        #enviar formulario
    if request.method == 'POST':
        value = request.POST['option']
        # ver opcion elegida
        if value == "1": d = solver_data['res_1']
        elif value == "2": d = solver_data['res_2']
        else: d = solver_data['res_3']
        #crear opcion
        option = Option.objects.update_or_create(user=request.user,
            defaults={"saving": d['saving'], "other": d['other'],
            "emergency": d['emergency'], "months": d['months']})
        if option:
            return redirect('profile')
    
    return render(request, "results.html", solver_data)

@login_required(login_url='login')
def profile(request):
    financial_info = request.user.financial_set.first()
    if not financial_info: # si no llena encuesta
        return redirect('survey')
    user_option = request.user.option_set.first()
    if not user_option: # si no tiene opcion elegida
        return redirect('results')

    pie_expenses_data = financial_info.pie_expenses_data()
    bars_dd_data = financial_info.bars_dd_data()
    bars_goal_data = user_option.bars_goal_data()
    data = {'user_option': user_option, 'bars_dd_data': bars_dd_data,
            'user_plan': user_option.msg(), 'bars_goal_data': bars_goal_data,
            'pie_expenses_data': pie_expenses_data}
    return render(request, "profile.html", data)

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
                return redirect('profile')

    return render(request, "login.html", {'form': form})

def logout(request):
    do_logout(request)
    return redirect('index')