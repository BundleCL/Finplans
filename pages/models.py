from django.db import models
from django.contrib.auth.models import User
from .constants import OBJ_CHOICES, ALERT_TYPES, COMM_TYPE

# Create your models here.
class Financial(models.Model):
    # Income
    fixed_income = models.IntegerField()
    fixed_income2 = models.IntegerField()
    fixed_income3 = models.IntegerField()
    extra_income = models.IntegerField()
    # Family expenses
    food_expenses = models.IntegerField()
    transport_expenses = models.IntegerField()
    health_expenses = models.IntegerField()
    education_expenses = models.IntegerField()
    clothing_expenses = models.IntegerField()
    subscription_expenses = models.IntegerField()
    # Home expenses
    rent_expenses = models.IntegerField()
    common_expenses = models.IntegerField()
    billing_expenses = models.IntegerField()
    phone_cable_internet_expenses = models.IntegerField()
    insurance_expenses = models.IntegerField()
    # Entertainment expenses
    entertainment_expenses = models.IntegerField()
    objective = models.CharField(max_length = 100, choices = OBJ_CHOICES)
    obj_savings = models.IntegerField()
    obj_months = models.IntegerField()
    extra_expenses = models.IntegerField()
    emergency_fund = models.IntegerField()
    alert_freq = models.IntegerField()
    alert_type = models.CharField(max_length = 100, choices = ALERT_TYPES)
    media = models.CharField(max_length = 20, choices = COMM_TYPE) 
    phone_number = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_meta(self):
        return self.obj_savings
    
    def get_plazo(self):
        return self.obj_months

    def get_DD(self):
        income = self.fixed_income + self.fixed_income2 + self.fixed_income3 + self.extra_income
        expenses = (self.food_expenses + self.transport_expenses + self.health_expenses +
        self.education_expenses + self.clothing_expenses + self.subscription_expenses +
        self.rent_expenses + self.common_expenses + self.billing_expenses +
        self.phone_cable_internet_expenses + self.insurance_expenses + self.entertainment_expenses)
        return income - expenses
    
    def get_Gm(self):
        return self.extra_expenses

    def get_F(self):
        return self.emergency_fund


class Option(models.Model):
    saving = models.IntegerField()
    other = models.IntegerField()
    emergency = models.IntegerField()
    months = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Tu meta de ahorro es $ %s, Fondo emergencia %s, \
            Otros gastos: %s en un plazo de %s meses" % (
            self.saving, self.emergency, self.other, self.months)
