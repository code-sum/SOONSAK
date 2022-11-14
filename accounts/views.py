from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth import authenticate, update_session_auth_hash, get_user_model
from django.contrib.auth import login as user_login
from django.contrib.auth import logout as user_logout
from django.contrib.auth.forms import AuthenticationForm

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
    user_followers = user.followings.count()
    context = {
        'user': user,
        'user_followers':user_followers,
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
def passwordchange(request, user_pk):
    user = User.objects.get(pk=user_pk)
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 비밀번호 바뀌면 로그인 상태 유지
            update_session_auth_hash(request, request.user)

            return redirect("accounts:detail", user_pk)
    
    else:
        form = PasswordChangeForm(request.user)

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