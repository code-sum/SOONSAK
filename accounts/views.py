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

def index(request):
    return render(request, 'accounts/index.html')

# 회원가입
def signup(request):

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.address = request.POST.get('postcode') + request.POST.get('address') + request.POST.get('detailAddress') + request.POST.get('extraAddress')
            user.save()
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
    # 사용자의 팔로워 사람
    user_followings = user.followings.count()
    # 사용자가 팔로잉하고 있는 사람
    user_followers = user.followers.count()
    # 사용자가 작성한 리뷰
    user_reviews = Review.objects.filter(user__id=user_pk)
    # 사용자가 구매목록
    user_orders = Order.objects.filter(user__id=user_pk)
    # 사용자가 좋아요한 상품
    
    context = {
        'user': user,
        'user_followings':user_followings,
        'user_followers':user_followers,
        'reviews':user_reviews,
        'orders':user_orders,
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
def follow(request, user_pk):
    user = User.objects.get(pk=user_pk)
    # 자기자신은 팔로우 못함
    if request.user in user.followings.all():
        user.followings.remove(request.user)
    else:
        user.followings.add(request.user)

        
    return redirect('accounts:detail', user_pk)


    # def follow(request, pk):
    # user = User.objects.get(pk=user_pk)
    # if request.user in user.followers.all():
    #     user.followers.remove(request.user)
    # else:
    #     user.followers.add(request.user)
    # return redirect('accounts:detail', pk)

# 고객센터
def cs(request):
    return render(request, 'accounts/cs.html')