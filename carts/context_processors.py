from .models import CartItem

def counter(request):
    item_count = 0
    if 'admin' in request.user.username:
        return {}
    
    try:
        cart_items = CartItem.objects.all().filter(user__id=request.user.pk)
        for cart_item in cart_items:
            item_count += cart_item.quantity

    except cart_items.DoesNotExist:
        item_count = 0

    return {"item_count": item_count}