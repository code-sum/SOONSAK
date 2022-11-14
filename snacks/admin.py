from django.contrib import admin
from .models import Snack,snack_Category

# Register your models here.

admin.site.register(Snack)
admin.site.register(snack_Category)