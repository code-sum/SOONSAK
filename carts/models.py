from django.db import models
from django.contrib.auth import get_user_model
from snacks.models import Snack
# 장바구니 모델

User = get_user_model()

class CartItem(models.Model):
    # 장바구니 사용자
    user = models.ForeignKey(User, related_name='user_cart', on_delete=models.CASCADE)
    # 장바구니에 담을 스냇종류
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)
    # 장바구니에 담을 양
    quantity = models.PositiveIntegerField()
    # 재고랑 비교해서 장바구니에 담을 수 있는지 확인
    activate = models.BooleanField(default=True)

    class Meta:
        # db 테일명 'CartItem'로 설정
        db_table = 'CartItem'
    # 장바구니에 담은 품목별로 결제 금액
    def sub_total(self):
        return self.snack.price * self.quantity
    # 장바구니에 담긴 총 결제 금액
    def total(self):
        total = 0
        for snack in self.snack:
            total += snack.quantity
        return total