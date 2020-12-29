from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Financial(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
    objective = models.TextField()
    obj_savings = models.IntegerField()
    obj_months = models.IntegerField()
    extra_expenses = models.IntegerField()
    emergency_fund = models.IntegerField()
    alert_freq = models.IntegerField()
    alert_type = models.TextField()
    media = models.TextField()
    phone_number = models.CharField()

class Option(models.Model):
    saving = models.IntegerField()
    other = models.IntegerField()
    emergency = models.IntegerField()
    months = models.IntegerField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Ahorro: %s, Fondo emergencia %s, Otros: %s y Plazo: %s" % (
            self.saving, self.emergency, self.other, self.months)
