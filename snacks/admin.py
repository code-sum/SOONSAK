from django.contrib import admin
from .models import Snacks,snack_Category

# Register your models here.
admin.site.register(Snacks)
admin.site.register(snack_Category)