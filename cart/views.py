from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from menu.models import MenuItem
from .models import Cart, CartItem

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
def add_to_cart(request, menu_item_id):
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'{menu_item.name} added to cart.')
    return redirect('cart:cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:cart_detail')

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0 and quantity <= cart_item.menu_item.quantity:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            messages.error(request, 'Invalid quantity requested.')
    except ValueError:
        messages.error(request, 'Invalid quantity value.')
    return redirect('cart:cart_detail')
