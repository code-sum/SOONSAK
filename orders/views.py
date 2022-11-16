from django.shortcuts import render, redirect
from snacks.models import Snack
from carts.models import CartItem
from .models import Order
from django.db import transaction
from django.utils import timezone

# 주문생성
def create(request):
    # 배송지 생성
    shipping_address = request.user.address
    shipping_phoneNum = request.user.phone_num
    # 로그인한 사용자의 장바구니
    cart_items = CartItem.objects.filter(user__id=request.user.pk)
    # 장바구니에 담긴 상품의 총 합계 => 결제금액 계산
    total_price = 0
    for each_total in cart_items:
        total_price += each_total.snack.price * each_total.quantity
    # 배송비 계산

    if total_price >= 50000:
        delivery_fee = 0
        billing_amount = total_price + delivery_fee
    else:
        delivery_fee = 3000
        billing_amount = total_price + delivery_fee
        # 주문서 작성
    if cart_items is not None:
        context = {
            "cart_items": cart_items,
            "total_price": total_price,
            "shipping_address": shipping_address,
            "shipping_phoneNum": shipping_phoneNum,
            "delivery_fee": delivery_fee,
            "billing_amount": billing_amount,
        }

    return render(request, "orders/create.html", context)


# 주문 완료
def order(request):

    cart_items = CartItem.objects.filter(user__id=request.user.pk)
    shipping_address = request.GET.get("shipping_address")
    contact_number = request.GET.get("contact_number")

    for cart_item in cart_items:

        snack = cart_item.snack
        quantity = cart_item.quantity

        with transaction.atomic():
            order = Order(
                user=request.user,
                snack=snack,
                quantity=quantity,
                shipping_address=shipping_address,
                contact_number=contact_number,
            )
            order.save()

            snack.stock -= int(quantity)
            snack.save()

    cart_items.delete()
    return render(request, "orders/orderComplete.html")


# 주문 상세
def detail(request, user_pk):
    # 결제 완료된 주문들
    complete_orders = Order.objects.filter(
        user__id=user_pk, order_status="결제완료"
    ).order_by("-register_data")
    # 취소된 주문들
    cancel_orders = Order.objects.filter(
        user__id=user_pk, order_status="취소주문"
    ).order_by("-register_data")
    # 누적 주문금액
    accumulated_amount = 0
    orders = Order.objects.filter(user__id=user_pk)
    for order in orders:
        if order.order_status == "결제완료":
            accumulated_amount += int(order.snack.price * order.quantity)

    context = {
        "complete_orders": complete_orders,
        "cancel_orders": cancel_orders,
        "accumulated_amount": accumulated_amount,
    }
    return render(request, "orders/detail.html", context)


# 배송 상태 변경
def delivery(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    order.register_data = timezone.now()
    with transaction.atomic():
        order.order_status = "배송 준비중"
        order.save()
    return redirect("orders:order_list")


# 배송 완료
def delivery_complete(request, order_pk):
    order = Order.objects.get(pk=order_pk)
    order.register_data = timezone.now()
    with transaction.atomic():
        order.order_status = "배송완료"
        order.save()
    return redirect("orders:order_list", request.user.pk)


# 주문 취소
def delete(request, order_pk):
    # 취소할 주문 가져오기
    order = Order.objects.get(pk=order_pk)
    # 주문 취소할 상품 가져오기
    snack = Snack.objects.get(pk=order.snack.pk)
    # 주문시간=> 취소시간 변경
    order.register_data = timezone.now()
    with transaction.atomic():
        # 취소할 상품 재고 채우기
        snack.stock += order.quantity
        snack.save()
        # 취소한 주문 상태 취소 주문으로 바꾸기
        order.order_status = "취소주문"
        order.save()
    if request.user.is_staff == 1:
        return redirect("orders:order_list")
    else:
        return redirect("orders:detail", request.user.pk)


# 주문 변경
def update(request, order_pk):
    # 주소지 변경할 주문 가져오기
    order = Order.objects.get(pk=order_pk)

    # 주소 변경 반영
    if request.method == "POST":
        order.shipping_address = request.POST.get("shipping_address")
        order.contact_number = request.POST.get("contact_number")
        order.save()
        return redirect("orders:detail", request.user.pk)
    else:
        shipping_address = order.shipping_address
        contact_number = order.contact_number
    context = {
        "order": order,
        "shipping_address": shipping_address,
        "contact_number": contact_number,
    }
    return render(request, "orders/update.html", context)


# 관리자 주문 내역
def order_list(request):
    # 결제 완료된 주문들
    complete_orders = Order.objects.filter(order_status="결제완료").order_by(
        "-register_data"
    )
    # 취소된 주문들
    cancel_orders = Order.objects.filter(order_status="취소주문").order_by("-register_data")
    # 배송 준비중인 주문들
    delivery_orders = Order.objects.filter(order_status="배송 준비중").order_by(
        "-register_data"
    )
    # 배송 완료된 주문들
    delivery_complete_orders = Order.objects.filter(order_status="배송완료").order_by(
        "-register_data"
    )
    context = {
        "complete_orders": complete_orders,
        "cancel_orders": cancel_orders,
        "delivery_orders": delivery_orders,
        "delivery_complete_orders": delivery_complete_orders,
    }
    return render(request, "orders/order_list.html", context)
