from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart
from .models import Order, OrderItem
from django.db import transaction
from django.core.exceptions import ValidationError

@login_required
def checkout(request):
    cart = Cart.objects.filter(user=request.user, completed=False).first()
    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        try:
            with transaction.atomic():
                # Create order
                order = Order.objects.create(
                    user=request.user,
                    total_amount=cart.get_total_price(),
                    shipping_address=request.POST.get('address'),
                    phone_number=request.POST.get('phone'),
                    email=request.POST.get('email')
                )

                for cart_item in cart.items.select_related('menu_item'):
                    menu_item = cart_item.menu_item
                    if menu_item.quantity < cart_item.quantity:
                        raise ValidationError(f"Not enough stock for {menu_item.name}")

                    # Reduce stock
                    menu_item.quantity -= cart_item.quantity
                    menu_item.save()

                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        menu_item=menu_item,
                        quantity=cart_item.quantity,
                        price=menu_item.price
                    )

                # Mark cart as completed
                cart.completed = True
                cart.save()

                messages.success(request, 'Order placed successfully!')
                return redirect('checkout:order_confirmation', order_id=order.id)

        except ValidationError as e:
            messages.error(request, str(e))
            return redirect('cart:cart_detail')

    return render(request, 'checkout/checkout.html', {'cart': cart})


@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'checkout/confirmation.html', {'order': order})
