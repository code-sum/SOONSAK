from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # 인덱스
    path('', views.index, name="index"),
    # 사용자 회원가입
    path('signup/', views.signup, name="signup"),
    # 사용자 로그인
    path('login/', views.login, name="login"),
    # 사용자 로그아웃
    path('logout/', views.logout, name="logout"),
    # 회원 프로필_이미지
    path('<int:user_pk>/', views.detail, name="detail"),
    # 회원 프로필 수정
    path('<int:user_pk>/update/', views.update, name="update"),
    # 회원 탈퇴
    path('<int:user_pk>/delete/', views.delete, name="delete"),
    # 비밀번호 변경
    path('<int:user_pk>/passwordchange', views.passwordchange, name="passwordchange"),
    # 팔로우
    path('<int:user_pk>/follow/', views.follow, name="follow"),
    # 고객센터
    path('cs/', views.cs, name='cs'),
]