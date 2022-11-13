from django.db import models
from django.contrib.auth import get_user_model
from snacks.models import Snack

# 결제앱
User = get_user_model()

class Order(models.Model):

    #결제하는 사용자
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # 주문할 상품
    snack = models.ForeignKey(Snack, on_delete=models.CASCADE)
    # 주문할 양
    quantity = models.PositiveIntegerField()
    # 배송지
    shipping_address = models.CharField(max_length=250)
    # 주문 시간
    register_data = models.DateTimeField(auto_now_add=True)
    # 주문 상탱
    order_status = models.CharField(max_length=250, default="결제완료")
    # 연락처
    contact_number = models.CharField(max_length=250, null=True)
    # 결제금액
    def total(self):
        total = 0
        total = self.snack.price * self.quantity
        return total
    