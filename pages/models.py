import json
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from .constants import OBJ_CHOICES, ALERT_TYPES, COMM_TYPE, COMM_FREQ

# Create your models here.
class Financial(models.Model):
    # Income
    fixed_income = models.IntegerField()
    fixed_income2 = models.IntegerField(default=0, blank=True, null=True)
    fixed_income3 = models.IntegerField(default=0, blank=True, null=True)
    extra_income = models.IntegerField(default=0, blank=True, null=True)
    # Family expenses
    food_expenses = models.IntegerField(default=0, blank=True, null=True)
    transport_expenses = models.IntegerField(default=0, blank=True, null=True)
    health_expenses = models.IntegerField(default=0, blank=True, null=True)
    education_expenses = models.IntegerField(default=0, blank=True, null=True)
    clothing_expenses = models.IntegerField(default=0, blank=True, null=True)
    subscription_expenses = models.IntegerField(default=0, blank=True, null=True)
    # Home expenses
    rent_expenses = models.IntegerField(default=0, blank=True, null=True)
    common_expenses = models.IntegerField(default=0, blank=True, null=True)
    billing_expenses = models.IntegerField(default=0, blank=True, null=True)
    telecom_expenses = models.IntegerField(default=0, blank=True, null=True)
    insurance_expenses = models.IntegerField(default=0, blank=True, null=True)
    # Entertainment expenses
    entertainment_expenses = models.IntegerField(default=0, blank=True, null=True)
    objective = models.CharField(max_length = 100, choices = OBJ_CHOICES)
    obj_savings = models.IntegerField()
    obj_months = models.IntegerField()
    extra_expenses = models.IntegerField()
    emergency_fund = models.IntegerField(default=0, blank=True, null=True)
    alert_freq = models.CharField(max_length = 100, choices = COMM_FREQ)
    alert_type = MultiSelectField(max_length = 255, choices = ALERT_TYPES)
    media = MultiSelectField(max_length = 255, choices = COMM_TYPE) 
    phone_number = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        # pylint: disable=E1101
        usr = self.user
        return f'Datos financieros de {usr.first_name} {usr.last_name}'

    def get_totals(self):
        income = self.fixed_income + self.fixed_income2 + self.fixed_income3 + self.extra_income
        expenses = (self.food_expenses + self.transport_expenses + self.health_expenses +
        self.education_expenses + self.clothing_expenses + self.subscription_expenses +
        self.rent_expenses + self.common_expenses + self.billing_expenses +
        self.telecom_expenses + self.insurance_expenses + self.entertainment_expenses)
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
            {"name": "Telecomunicaciones", "y": self.telecom_expenses},
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
        # pylint: disable=E1101
        usr = self.user
        return f'Meta financiera de {usr.first_name} {usr.last_name}'

    def msg(self):
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
