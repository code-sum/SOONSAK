from django.shortcuts import render, get_object_or_404, redirect
from .models import CartItem
from django.contrib.auth import get_user_model
from snacks.models import Snack
from django.http import Http404
from django.contrib.auth.decorators import login_required


User = get_user_model()

#상품 장바구니에 상품 추가
@login_required(login_url="accounts:login")
def add_cart(request, snack_pk):
    # 장바구니에 담을 상품 가져오기
    snack = Snack.objects.get(pk=snack_pk)

    # 하나씩 담기
    if 'quantity' in request.GET:
        cart = CartItem.objects.get(snack__id=snack.pk, user__id=request.user.pk)
        
        cart.quantity += 1
        cart.save()
        return redirect('carts:my_cart')
    
    # 이미 장바구니가 있다면 장바구니 가져오기
    try:
        cart = CartItem.objects.get(snack__pk=snack_pk, user__id=request.user.pk)
                
        if cart:
            # 만약에 상품이 이름이 카트에 담긴 상품과 이름이 같다면
            if cart.snack.name == snack.name:
                cart.quantity += int(request.POST['quantity'])
                cart.save()
    # 장바구니가 없다면 새로 만들어서 저장
    except CartItem.DoesNotExist:
        user = User.objects.get(pk=request.user.pk)
        cart = CartItem(
            user = user,
            snack = snack,
            quantity = int(request.POST['quantity'])
        )    
        cart.save()
    return redirect('carts:my_cart')

# 나의 장바구니
@login_required(login_url="accounts:login")
def my_cart(request):
    # 사용자의 장바구니 가져오기 
    cart_items = CartItem.objects.filter(user__id=request.user.pk)
    print(cart_items)
    # 주문 금액 계산
    total_price = 0
    for each_total in cart_items:
        total_price += each_total.snack.price * each_total.quantity
    
    if cart_items is not None:
        context = {
            'cart_items':cart_items,
            'total_price':total_price,
        }
        return render(request, 'carts/my_cart.html', context)

# 장바구니에서 삭제
@login_required(login_url="accounts:login")    
def minus_cart_item(request, snack_pk):
    # 뺄 상품이 들어있는 장바구니 가져오기
    cart_item = CartItem.objects.filter(snack__id=snack_pk)
    snack = Snack.objects.get(pk=snack_pk)
    # 권한 메시지

    try:
        for item in cart_item:
            if item.snack.name == snack.name:
                if item.quantity > 1:
                    item.quantity -= 1
                    item.save()
                    
                elif item.quantity == 1:
                    item.delete()
            
                return redirect('carts:my_cart')
    except CartItem.DoesNotExist:
        raise Http404
        


# 장바구니에서 품목 전체 삭제
@login_required(login_url="accounts:login")
def full_remove(request, snack_pk):
    snack = get_object_or_404(Snack, pk=snack_pk)
    cart_item = CartItem.objects.get(snack__id=snack.pk, user__id=request.user.pk)
    cart_item.delete()
    return redirect('carts:my_cart')