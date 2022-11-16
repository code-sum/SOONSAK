from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from reviews.models import Review
from orders.models import Order
from reviews.models import Comment
from snacks.models import Snack
from django.views.decorators.http import require_POST, require_safe
from django.http import JsonResponse
from django.db.models import Count

def index(request):
    return render(request, 'accounts/index.html')

# 회원가입
def signup(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # 자동 로그인 
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            user_login(request, user)
            return redirect('/')
        
    else:
        form = CustomUserCreationForm()
    
    context = {
        'form':form
    }
    return render(request, 'accounts/signup.html', context)

# 로그인
def login(request):

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_login(request, form.get_user())
            return redirect('/')
    else:
        form = AuthenticationForm()

    context ={
        'form':form,
    }
    return render(request, 'accounts/login.html', context)

# 로그아웃
def logout(request):

    user_logout(request)

    return redirect("/")

# 회원 상세 정보
def detail(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    # 사용자가 작성한 리뷰
    user_reviews = Review.objects.filter(user__id=user_pk)
    # 사용자가 작성한 댓글
    user_comments = Comment.objects.filter(user__id=user_pk)
    # 사용자 구매내역
    user_orders = Order.objects.filter(user__id=user_pk)
    # 사용자가 찜한 상품
    likes_snacks = Snack.objects.all().filter(likes__id=user_pk)
    # 활동지수(리뷰갯수 + 팔로워수 + 댓글수)
    user_of_reviews = Review.objects.filter(user__id=user_pk).count()
    user_of_followers = User.objects.filter(followings=user.pk).count()
    user_of_comments = Comment.objects.filter(user__id=user_pk).count()
    active_index = user_of_reviews + user_of_followers + user_of_comments
    
    context = {
        'user': user,
        'user_reviews': user_reviews,
        'user_orders': user_orders,
        'user_comments':user_comments,
        'likes_snacks':likes_snacks,
        'active_index':active_index,
    }
    return render(request, 'accounts/detail.html', context)

# 회원 프로필 수정
def update(request, user_pk):

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }

    return render(request, 'accounts/update.html', context)

# 회원 탈퇴
def delete(request, user_pk):

    user = User.objects.get(pk=user_pk)
    user.delete()
    user_logout(request)
    return redirect('/')    


# 회원 비밀번호 변경
@login_required
def passwordchange(request, user_pk):    
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 비밀번호 바뀌면 로그인 상태 유지
            update_session_auth_hash(request, request.user)
            return redirect("accounts:detail", user_pk)
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request, 'accounts/passwordchange.html', context)

# 팔로우
@require_POST
def follow(request, user_pk):
    if request.user.is_authenticated:
        User = get_user_model()
        me = request.user
        you = User.objects.get(pk=user_pk)
        if me != you:
            if you.followers.filter(pk=me.pk).exists():
                you.followers.remove(me)
                is_followed = False
            else:
                you.followers.add(me)
                is_followed = True
            context = {
                "is_followed": is_followed,
                "followers_count": you.followers.count(),
                "followings_count": you.followings.count(),
            }
            return JsonResponse(context)
        return redirect("accounts:detail", you.username)
    return redirect("accounts:login")

# 고객센터
def cs(request):
    return render(request, 'accounts/cs.html')