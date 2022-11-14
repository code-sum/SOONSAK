from django.contrib import admin
from .models import Snacks,snack_Category

# Register your models here.
# admin에서 모델이 보이도록
admin.site.register(Snacks)
admin.site.register(snack_Category)