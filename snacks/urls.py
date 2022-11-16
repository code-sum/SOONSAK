from django.urls import path
from . import views

app_name = 'snacks'

urlpatterns = [
  # 카테고리 등록
  path("category_create/", views.category_create, name="category_create"),
  # 상품 전체 조회
  path("", views.index, name="index"),
  # 상품 등록
  path("create/", views.create, name="create"),
  # 상품 상세조회
  path("detail/<int:snack_pk>", views.detail, name="detail"),
  # 상품 수정
  path("update/<int:snack_pk>", views.update, name="update"),
  # 상품 삭제
  path("delete/<int:snack_pk>", views.delete, name="delete"),
  # 상품 좋아요
  path("likes/<int:snack_pk>/", views.likes, name="likes"),
  # 상품 카테고리 검색
  path("search/<str:kw>/", views.search, name="search"),
  # 상품 검색어 검색
  path("search_kwargs/", views.search_kwargs, name="search_kwargs"),
]