from django.shortcuts import render
from .models import Snacks, snack_Category
from accounts.models import User

# Create your views here.

# detail 시작
def detail(request,snack_pk):
    snack = Snacks.objects.get(pk=snack_pk)
    category = snack_Category.objects.get(pk=snack.pk)
    context = {
        "snack": snack,
        "category": category
    }
    return render(request, "snacks/detail.html", context)
# detail 종료

# delete 시작
def delete(request, snack_pk):
    snack = Snacks.objects.get(pk=snack_pk)
    snack.delete()
    return render(request, "snacks/index.html")
# delete 종료