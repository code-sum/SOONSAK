from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path('', views.index, name='index'),
    # 리뷰 작성
    path('<int:snack_pk>/create/', views.create, name='create'),
    # 리뷰 상세
    path('<int:review_pk>/', views.detail, name='detail'),
    # 리뷰 수정
    path('<int:review_pk>/update/', views.update, name='update'),
    # 리뷰 삭제
    path('<int:review_pk>/delete/', views.delete, name='delete'),
    # 댓글 생성
    path('<int:review_pk>/add_comment/', views.add_comment, name='add_comment'),
    # 댓글 삭제
    path('<int:review_pk>/delete_comment/<int:comment_pk>/', views.delete_comment, name='delete_comment'),
]