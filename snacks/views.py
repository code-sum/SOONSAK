from django.shortcuts import render, redirect, get_object_or_404
from .models import Snack
from reviews.models import Review
from carts.forms import CartForm
from .forms import SnackForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# 상품 메뉴 전체 조회
def index(request):
    snacks = Snack.objects.all()

    context = {
        'snacks':snacks,
    }
    return render(request, 'snacks/index.html', context)

# 상품 카테고리 등록
@login_required(login_url='accounts:login')
def category_create(request):
    # 관리자 권한을 가진 사용자만 상품을 등록할 수 있다.
    if request.user.is_staff:
        if request.method == "POST":
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = CategoryForm()
        context = {
            'form':form,
        }
        return render(request, 'snacks/category_create.html', context)
    # 관리자가 아니라면 권한 오류 메시지
    else:
        messages.error(request, "권한이 없습니다.")
        return redirect("/")



# 상품 메뉴 등록
@login_required(login_url='accounts:login')
def create(request):
    # 관리자 권한을 가진 사용자만 상품을 등록할 수 있다.
    if request.user.is_staff:
        if request.method == "POST":
            form = SnackForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                return redirect('/')
        else:
            form = SnackForm()
        context = {
            'form':form,
        }
        return render(request, 'snacks/create.html', context)
    # 관리자가 아니라면 권한 오류 메시지
    else:
        messages.error(request, "권한이 없습니다.")
        return redirect("/")
    
# 상품 메뉴 상세조회
def detail(request,snack_pk):
    snack = get_object_or_404(Snack, pk=snack_pk)
    # 상품 리뷰들 
    reviews = Review.objects.filter(snack__pk=snack_pk)
    # 장바구니 폼
    form = CartForm()
    context = {
        "snack": snack,
        "reviews":reviews,
        'form': form,
    }
    return render(request, "snacks/detail.html", context)


# 상품 수정
@login_required(login_url='accounts:login')
def update(request, snack_pk):
    snack = get_object_or_404(Snack, pk=snack_pk)
    # 관리자 권한을 가진 사용자만 상품을 수정할 수 있다.
    if request.user.is_staff:
        if request.method == "POST":
            form = SnackForm(request.POST, request.FILES, instance=snack)
            if form.is_valid():
                form.save()
                return redirect('snacks:index')
        else:
            form = SnackForm(instance=snack)
        context = {
            'form':form,
        }
        return render(request, 'snacks/update.html', context)
    # 관리자가 아니라면 권한 오류 메시지
    else:
        messages.error(request, "권한이 없습니다.")
        return redirect("snacks:index")

# 상품 삭제
def delete(request, snack_pk):
    snack = get_object_or_404(Snack, pk=snack_pk)
    snack.delete()
    return redirect("snacks:index")
