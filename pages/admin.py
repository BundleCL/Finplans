from django.contrib import admin
from pages.models import Financial, Option

# Register your models here.
admin.site.register([Financial, Option])