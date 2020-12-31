from django.contrib import admin
from pages.models import Financial, Option


@admin.register(Financial)
class FinancialAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name',)