from django.shortcuts import render, redirect, get_object_or_404
from .models import Snack
from .models import snack_Category 
from reviews.models import Review
from carts.forms import CartForm
from .forms import SnackForm, CategoryForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Avg, Count, Q

# 상품 메뉴 전체 조회
def index(request):
    snacks = Snack.objects.all()
    # 찜 많은순
    snack_like = Snack.objects.all().annotate(like_cnt=Count('likes')).order_by('-like_cnt')
    # 최신순
    snack_id = Snack.objects.all().order_by('-id')
    # 리뷰 많은 순
    snack_reviews = Snack.objects.all().prefetch_related('snack_review').annotate(review_cnt=Count('snack_review')).order_by('-review_cnt')
    # 카테고리
    snack_category = snack_Category.objects.all()
   
    context = {
        'snacks':snacks,

        "snack_id": snack_id,
       
        'snack_category ':snack_category,        

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
    # 장바구니 폼
    form = CartForm()
     # 평균 별점
    try:    
        snack_avg = Review.objects.filter(snack__pk=snack_pk).aggregate(Avg('grade'))
        
        if snack_avg['grade__avg'] > 4.9:
            avg_star = "⭐⭐⭐⭐⭐"
        elif snack_avg['grade__avg'] > 4.4:
            avg_star = "⭐⭐⭐⭐☆"
        elif snack_avg['grade__avg'] > 3.9:
            avg_star = "⭐⭐⭐⭐"
        elif snack_avg['grade__avg'] > 3.4:
            avg_star = "⭐⭐⭐☆"
        elif snack_avg['grade__avg'] > 2.9:
            avg_star = "⭐⭐⭐"
        elif snack_avg['grade__avg'] > 2.4:
            avg_star = "⭐⭐☆"
        elif snack_avg['grade__avg'] > 1.9:
            avg_star = "⭐⭐"
        elif snack_avg['grade__avg'] > 1.4:
            avg_star = "⭐☆"
        elif snack_avg['grade__avg'] > 0.9:
            avg_star = "⭐"
        elif snack_avg['grade__avg'] > 0.4:
            avg_star = "☆"
        else:
            avg_star = "별점 없음"
        snack_avg = round(snack_avg['grade__avg'],2)
    except:
        avg_star = ""
        snack_avg = "리뷰 없음"
    # 장바구니 폼
    form = CartForm()
    context = {
        "snack": snack,
        "reviews":reviews,
        'form': form,        
        "snack_avg": snack_avg,
        "avg_star":avg_star,
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
        existed_user = False
    else:
        snack.likes.add(request.user)
        existed_user = True
    likeCount = snack.likes.count()
    
    context = {
        "existed_user" : existed_user,
        "likeCount" : likeCount,
    }
    
    return JsonResponse(context)


# 상품 카테고리 검색
def search(request, kw):
    query = kw
    snack_category = snack_Category.objects.get(category=query)
    snacks = Snack.objects.filter(category__id=snack_category)
    context = {
        'snacks':snacks,
    }
    return render(request, 'snacks/search.html', context)

# 상품 카테고리 검색
def search_kwargs(request):
    if 'kw' in request.POST:
        query = request.POST.get('kw')
        snacks = Snack.objects.filter(Q(name__icontains=query) | Q(category__category=query)).annotate(like_cnt=Count('likes')).order_by('-like_cnt')
    context = {
        'snacks':snacks
    }
    return render(request, 'snacks/search.html', context)