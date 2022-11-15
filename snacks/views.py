from django.shortcuts import render, redirect, get_object_or_404
from .models import Snack
from reviews.models import Review
from accounts.models import User
from carts.forms import CartForm
from .forms import SnackForm, CategoryForm
from django.contrib.auth.decorators import login_required

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
    else:
        
        return redirect('/')
    
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
    
    else:
        return redirect('/')
    
    
# 상품 메뉴 상세조회
def detail(request,snack_pk):
    snack = get_object_or_404(Snack, pk=snack_pk)
    # 상품 리뷰들 
    reviews = Review.objects.filter(snack__pk=snack_pk).order_by('-pk')
    # 리뷰 작성자 프로필 불러오기
    users = User.objects.all()
    # 평균별점
    total = []
    cnt = 0
    for review in reviews:
        total.append(review.grade)
        cnt += 1
    star_avg = sum(total)/cnt

    # 리뷰 별점 가져오기
    star_dict = {
        5 : "⭐⭐⭐⭐⭐",
        4 : "⭐⭐⭐⭐",
        3 : "⭐⭐⭐",
        2 : "⭐⭐",
        1 : "⭐",
    }

    # 장바구니 폼
    form = CartForm()
    context = {
        "snack": snack,
        "reviews":reviews,
        'form': form,
        "users": users,
        "star_avg": int(star_avg),
        "star_dict":star_dict,
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
        return redirect('/')

# 상품 삭제
def delete(request, snack_pk):
    if request.user.is_staff:
        snack = get_object_or_404(Snack, pk=snack_pk)
        snack.delete()
        return redirect("snacks:index")
    else:
        return redirect('/')
    
# 상품 좋아요
def likes(request, snack_pk):
    snack = Snack.objects.get(pk=snack_pk)
    
    if request.user in snack.likes.all():
        snack.likes.remove(request.user)
    else:
        snack.likes.add(request.user)
        
    return redirect('snacks:detail',snack_pk)