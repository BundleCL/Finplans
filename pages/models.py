import json
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

    def get_totals(self):
        income = self.fixed_income + self.fixed_income2 + self.fixed_income3 + self.extra_income
        expenses = (self.food_expenses + self.transport_expenses + self.health_expenses +
        self.education_expenses + self.clothing_expenses + self.subscription_expenses +
        self.rent_expenses + self.common_expenses + self.billing_expenses +
        self.phone_cable_internet_expenses + self.insurance_expenses + self.entertainment_expenses)
        return (income, expenses)

    def get_meta(self):
        return self.obj_savings
    
    def get_plazo(self):
        return self.obj_months

    def get_DD(self):
        income, expenses = self.get_totals()
        return income - expenses
    
    def get_Gm(self):
        return self.extra_expenses

    def get_F(self):
        return self.emergency_fund
    
    def bars_dd_data(self):
        income, expenses = self.get_totals()
        bars_data = {
            "chart": {"type": "column"},
            "title": {"text": "Tu dinero disponible es $ %s"%f"{(income-expenses):,}".replace(",",".")},
            "xAxis": {"categories": ["Dinero disponible"]},
            "series": [{"name": "Ingresos fijos ($) ", "data": [income], "color": "#7ba3e3"},
            {"name": "Gastos fijos ($)", "data": [expenses],  "color": "#eb463d"}]
        }
        return json.dumps(bars_data)
    
    def pie_expenses_data(self):
        pie_data = {
            "chart": {"type": "pie"},
            "title": {"text": "Tus principales gastos son"},
            "tooltip": {"pointFormat": '{series.name}: <b>{point.percentage:.1f}%</b> <br>valor ($): {point.y}'},
            "accessibility": {"point": {"valueSuffix": '%'}},
            "plotOptions": {
                "pie": {"allowPointSelect": "true", "cursor": 'pointer', "showInLegend": "true",
                "dataLabels": {"enabled": "true", "format": '<b>{point.name}</b>:<br>{point.percentage:.1f} %'}}},
            "series": [{
                "name": "Gastos", "data": [
            {"name": "Arriendo", "y": self.rent_expenses},
            {"name": "Gastos comunes", "y": self.common_expenses},
            {"name": "Supermercado", "y": self.food_expenses},
            {"name": "Transporte", "y": self.transport_expenses},
            {"name": "Educación", "y": self.education_expenses},
            {"name": "Salud", "y": self.health_expenses},
            {"name": "Subscripciones", "y": self.subscription_expenses},
            {"name": "Cuentas", "y": self.billing_expenses},
            {"name": "Telecomunicaciones", "y": self.phone_cable_internet_expenses},
            {"name": "Seguros", "y": self.insurance_expenses},
            {"name": "Ropa", "y": self.clothing_expenses},
            {"name": "Entretención", "y": self.entertainment_expenses},]
            }]
        }
        return json.dumps(pie_data)


class Option(models.Model):
    saving = models.IntegerField()
    other = models.IntegerField()
    emergency = models.IntegerField()
    months = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Tu meta de ahorro es $ %s, con un fondo emergencia de $ %s.  \
            Además, cuentas con $ %s para otros gastos en un plazo de %s meses." % (
            f"{self.saving:,}".replace(",","."), f"{self.emergency:,}".replace(",","."),
            f"{self.other:,}".replace(",","."), self.months)
    
    def bars_goal_data(self):
        bars_data = {
            "chart": {"type": "column"},
            "title": {"text": "Tu plan de ahorro"},
            "xAxis": {"categories": ["Mes"]},
            "series": [{"data": [self.saving * i for i in range(1, self.months+2)],
                "color": "#7ba3e3", "name": "Monto ($)"}]
        }
        return json.dumps(bars_data)
