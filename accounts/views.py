from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from django.contrib.auth.forms import PasswordChangeForm
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
    CustomPasswordChangeForm,
)
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

# 회원가입
def signup(request):

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.address = (
                request.POST.get("postcode")
                + request.POST.get("address")
                + request.POST.get("detailAddress")
                + request.POST.get("extraAddress")
            )
            user.save()

            # 자동 로그인
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            user_login(request, user)
            return redirect("/")

    else:
        form = CustomUserCreationForm()

    context = {"form": form}
    return render(request, "accounts/signup.html", context)


# 로그인
def login(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user_login(request, form.get_user())
            return redirect("/")
    else:
        form = AuthenticationForm()

    context = {
        "form": form,
    }
    return render(request, "accounts/login.html", context)


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
    user_orders = Order.objects.filter(user__id=user_pk).order_by("-register_data")
    # 사용자의 팔로워 목록
    user_followers = user.followers.order_by("pk")
    # 사용자의 팔로잉 목록
    user_followings = user.followings.order_by("pk")
    # 활동지수(리뷰갯수 + 팔로워수 + 댓글수)
    user_of_reviews = Review.objects.filter(user__id=user_pk).count()
    user_of_followers = User.objects.filter(followings=user.pk).count()
    user_of_comments = Comment.objects.filter(user__id=user_pk).count()
    active_index = user_of_reviews + user_of_followers + user_of_comments

    context = {
        "user": user,
        "user_reviews": user_reviews,
        "user_orders": user_orders,
        "user_comments": user_comments,
        "user_followers": user_followers,
        "user_followings": user_followings,
        "active_index": active_index,
    }
    return render(request, "accounts/detail.html", context)


# 회원 프로필 수정
def update(request, user_pk):

    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            user = form.save(commit=False)
            user.address = (
                request.POST.get("postcode")
                + request.POST.get("address")
                + request.POST.get("detailAddress")
                + request.POST.get("extraAddress")
            )
            user.save()
            return redirect("accounts:detail", user_pk)

    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        "form": form,
    }

    return render(request, "accounts/update.html", context)


# 회원 탈퇴
def delete(request, user_pk):

    user = User.objects.get(pk=user_pk)
    user.delete()
    user_logout(request)
    return redirect("/")


# 회원 비밀번호 변경
@login_required
def passwordchange(request, user_pk):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            # 비밀번호 바뀌면 로그인 상태 유지
            update_session_auth_hash(request, request.user)
            return redirect("accounts:detail", user_pk)
    else:
        form = CustomPasswordChangeForm(request.user)
    context = {
        "form": form,
    }
    return render(request, "accounts/passwordchange.html", context)


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


def likelist(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    # 사용자가 찜한 상품
    likes_snacks = Snack.objects.all().filter(likes__id=user_pk)
    context = {
        "user": user,
        "likes_snacks": likes_snacks,
    }
    return render(request, "accounts/likelist.html", context)


# 고객센터
def cs(request):
    return render(request, "accounts/cs.html")


# 소셜 로그인 연동
import secrets, requests

state_token = secrets.token_urlsafe(16)

# 카카오 로그인
def kakao_request(request):
    kakao_api = "https://kauth.kakao.com/oauth/authorize?response_type=code"
    redirect_uri = "http://soonsak-env.eba-rnwyi2s3.ap-northeast-2.elasticbeanstalk.com/accounts/login/kakao/callback"
    client_id = "e354ba53e1c46a96b9483564296d7ca9"  # 배포시 보안적용 해야함
    return redirect(f"{kakao_api}&client_id={client_id}&redirect_uri={redirect_uri}")


def kakao_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "e354ba53e1c46a96b9483564296d7ca9",  # 배포시 보안적용 해야함
        "redirect_uri": "http://soonsak-env.eba-rnwyi2s3.ap-northeast-2.elasticbeanstalk.com/accounts/login/kakao/callback",
        "code": request.GET.get("code"),
    }
    kakao_token_api = "https://kauth.kakao.com/oauth/token"
    access_token = requests.post(kakao_token_api, data=data).json()["access_token"]

    headers = {"Authorization": f"bearer ${access_token}"}
    kakao_user_api = "https://kapi.kakao.com/v2/user/me"
    kakao_user_information = requests.get(kakao_user_api, headers=headers).json()

    kakao_id = kakao_user_information["id"]
    kakao_nickname = kakao_user_information["properties"]["nickname"]
    # 유저 모델에 프로필 사진 추가시 사용
    kakao_profile_image = kakao_user_information["properties"]["profile_image"]

    if get_user_model().objects.filter(kakao_id=kakao_id).exists():
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    else:
        kakao_login_user = get_user_model()()
        kakao_login_user.username = kakao_nickname
        kakao_login_user.kakao_id = kakao_id
        kakao_login_user.social_profile_picture = kakao_profile_image
        kakao_login_user.set_password(str(state_token))
        kakao_login_user.save()
        kakao_user = get_user_model().objects.get(kakao_id=kakao_id)
    user_login(request, kakao_user, "django.contrib.auth.backends.ModelBackend")
    return redirect(request.GET.get("next") or "/")


# 네이버 로그인
def naver_request(request):
    naver_api = "https://nid.naver.com/oauth2.0/authorize?response_type=code"
    client_id = "FuDxFWBVKojR52KP2ndd"  # 배포시 보안적용 해야함
    redirect_uri = "http://soonsak-env.eba-rnwyi2s3.ap-northeast-2.elasticbeanstalk.com/accounts/login/naver/callback"
    state_token = secrets.token_urlsafe(16)
    return redirect(
        f"{naver_api}&client_id={client_id}&redirect_uri={redirect_uri}&state={state_token}"
    )


def naver_callback(request):
    data = {
        "grant_type": "authorization_code",
        "client_id": "FuDxFWBVKojR52KP2ndd",  # 배포시 보안적용 해야함
        "client_secret": "8canpavPj_",
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "redirect_uri": "http://soonsak-env.eba-rnwyi2s3.ap-northeast-2.elasticbeanstalk.com/accounts/login/naver/callback",
    }
    naver_token_request_url = "https://nid.naver.com/oauth2.0/token"
    access_token = requests.post(naver_token_request_url, data=data).json()[
        "access_token"
    ]

    headers = {"Authorization": f"bearer {access_token}"}
    naver_call_user_api = "https://openapi.naver.com/v1/nid/me"
    naver_user_information = requests.get(naver_call_user_api, headers=headers).json()

    naver_id = naver_user_information["response"]["id"]
    naver_nickname = naver_user_information["response"]["name"]
    # 유저 모델에 프로필 사진 추가시 사용

    if get_user_model().objects.filter(naver_id=naver_id).exists():
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    else:
        naver_login_user = get_user_model()()
        naver_login_user.username = naver_nickname
        naver_login_user.naver_id = naver_id
        naver_login_user.set_password(str(state_token))
        naver_login_user.save()
        naver_user = get_user_model().objects.get(naver_id=naver_id)
    user_login(request, naver_user, "django.contrib.auth.backends.ModelBackend")
    return redirect(request.GET.get("next") or "/")


# 구글 로그인
def google_request(request):
    google_api = "https://accounts.google.com/o/oauth2/v2/auth"
    client_id = "184916314988-t244n3si5jvjidlulkuucmh1jclrkvfo.apps.googleusercontent.com"  # 배포시 보안적용 해야함
    redirect_uri = "https://soonsak-env.eba-rnwyi2s3.ap-northeast-2.elasticbeanstalk.com/accounts/login/google/callback"
    google_base_url = "https://www.googleapis.com/auth"
    google_email = "/userinfo.email"
    google_myinfo = "/userinfo.profile"
    scope = f"{google_base_url}{google_email}+{google_base_url}{google_myinfo}"
    return redirect(
        f"{google_api}?client_id={client_id}&response_type=code&redirect_uri={redirect_uri}&scope={scope}"
    )

def google_callback(request):
    data = {
        "code": request.GET.get("code"),
        "state": request.GET.get("state"),
        "grant_type": "authorization_code",
        "client_id": "184916314988-t244n3si5jvjidlulkuucmh1jclrkvfo.apps.googleusercontent.com",  # 배포시 보안적용 해야함
        "client_secret": "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",
        "redirect_uri": "https://soonsak-env.eba-rnwyi2s3.ap-northeast-2.elasticbeanstalk.com/accounts/login/google/callback",
    }
    google_token_request_url = "https://oauth2.googleapis.com/token"
    access_token = requests.post(google_token_request_url, data=data).json()[
        "access_token"
    ]
    params = {
        "access_token": f"{access_token}",
    }
    google_call_user_api = "https://www.googleapis.com/oauth2/v3/userinfo"
    google_user_information = requests.get(google_call_user_api, params=params).json()

    googld_id = google_user_information["sub"]
    googld_name = google_user_information["name"]
    googld_email = google_user_information["email"]
    googld_picture = google_user_information["picture"]
    print(googld_id)
    if get_user_model().objects.filter(googld_id=googld_id).exists():
        google_user = get_user_model().objects.get(googld_id=googld_id)
    else:
        google_login_user = get_user_model()()
        google_login_user.username = googld_name
        google_login_user.email = googld_email
        google_login_user.social_profile_picture = googld_picture
        google_login_user.googld_id = googld_id
        google_login_user.set_password(str(state_token))
        google_login_user.save()
        google_user = get_user_model().objects.get(googld_id=googld_id)
    user_login(request, google_user,  'django.contrib.auth.backends.ModelBackend')
    return redirect(request.GET.get("next") or "/")
