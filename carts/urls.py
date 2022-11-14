from django.urls import path
from . import views

app_name = 'carts'

urlpatterns = [
    # 장바구니
    path("my_cart/",views.my_cart, name="my_cart"),
    # 상품을 장바구니에 추가
    path("add/<int:snack_pk>/", views.add_cart, name="add_cart"),
    # 상품을 장바구니에서 빼기
    path("minus_cart_item/<int:snack_pk>/", views.minus_cart_item, name="minus_cart_item"),
    # 전체 삭제
    path("full_remove/<int:snack_pk>/", views.full_remove, name="full_remove"),
]