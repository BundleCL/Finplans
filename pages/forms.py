from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def check_mail(self, email):
        if (User.objects.filter(email=email).exists()):
            self.add_error('email', 'Este correo ya se ha registrado')
            return False
        return True

class FinancialDataForm(forms.ModelForm):

    # Income
    fixed_income = forms.IntegerField(min_value=0)
    fixed_income2 = forms.IntegerField(min_value=0)
    fixed_income3 = forms.IntegerField(min_value=0)
    extra_income = forms.IntegerField(min_value=0)

    # Family expenses
    food_expenses = forms.IntegerField(min_value=0)
    transport_expenses = forms.IntegerField(min_value=0)
    health_expenses = forms.IntegerField(min_value=0)
    education_expenses = forms.IntegerField(min_value=0)
    clothing_expenses = forms.IntegerField(min_value=0)
    subscription_expenses = forms.IntegerField(min_value=0)

    # Home expenses
    rent_expenses = forms.IntegerField(min_value=0)
    common_expenses = forms.IntegerField(min_value=0)
    billing_expenses = forms.IntegerField(min_value=0)
    phone_cable_internet_expenses = forms.IntegerField(min_value=0)
    insurance_expenses = forms.IntegerField(min_value=0)

    # Entertainment expenses
    entertainment_expenses = forms.IntegerField(min_value=0)

    OBJ_CHOICES = [
        (0, 'Comprar un departamento o casa'),
        (1, 'Pagar mi educación'),
        (2, 'Viajar'),
        (3, 'Emprender un negocio o nuevo proyecto'),
        (4, 'Para mi jubilación'),
        (5, 'Invertir mi dinero'),
        (6, 'Pagar algún tipo de seguro o deuda'),
        (7, 'Otro objetivo de ahorro'),
        (8, 'No tengo ningún objetivo de ahorro en mente')
    ] 
    objective = forms.ChoiceField(choices=OBJ_CHOICES)
    obj_savings = forms.IntegerField(min_value=0)
    obj_months = forms.IntegerField(min_value=0)
    extra_expenses = forms.IntegerField(min_value=0)
    emergency_fund = forms.IntegerField(min_value=0)

    alert_freq = forms.IntegerField(min_value=0)
    ALERT_TYPES = [
        (0, 'Saldo bajo en cuenta'),
        (1, 'Movimientos duplicados'),
        (2, 'Resumen semanal de tu control financiero'),
        (3, 'Resumen mensual de tu control financiero'),
        (4, 'Proyección del ahorro'),
        (5, 'Dinero restante por cumplir la cuota mensual de ahorro')
    ]
    alert_type = forms.ChoiceField(choices=ALERT_TYPES)
    COMM_TYPE = [
        (0, 'Whatsapp'),
        (1, 'Email')
    ]
    media = forms.ChoiceField(choices=COMM_TYPE)

    phone_number = forms.CharField()

    class Meta:
        model = User
        fields = ('fixed_income', 'fixed_income2', 'fixed_income3', 'extra_income',
        'food_expenses', 'transport_expenses', 'health_expenses', 'education_expenses',
        'clothing_expenses', 'subscription_expenses',
        'rent_expenses', 'common_expenses', 'billing_expenses', 'phone_cable_internet_expenses',
        'insurance_expenses', 'entertainment_expenses', 'objective', 'obj_savings', 'obj_months',
        'extra_expenses', 'emergency_fund', 'alert_freq', 'alert_type', 'media', 'phone_number')