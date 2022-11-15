from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # 주문서 생성
    path('create/', views.create, name="create"),
    # 주문 생성
    path('order/', views.order, name="order"),
    # 주문 내역
    path('detail/<int:user_pk>', views.detail, name="detail"),
    # 주문 취소
    path('delete/<int:order_pk>/', views.delete, name="delete"),
    # 주문 변경
    path('update/<int:order_pk>/', views.update, name="update"),
    # 관리자 주문 내역
    path('order_list/', views.order_list, name='order_list'),
    # 배송 준비중
    path('delivery/<int:order_pk>/', views.delivery, name='delivery'),
    # 배송 완료
    path('delivery_complete/<int:order_pk>/', views.delivery_complete, name='delivery_complete')
]