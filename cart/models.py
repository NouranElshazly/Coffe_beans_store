from django.db import models
from django.contrib.auth import get_user_model
from menu.models import MenuItem
from checkout.models import Order, OrderItem  # adjust import paths to your project structure
from django.db import transaction
from django.core.exceptions import ValidationError
User = get_user_model()

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)

    def get_total_price(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_total_items(self):
        return sum(item.quantity for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    def get_cost(self):
        return self.menu_item.price * self.quantity

    def is_available(self):
        return self.menu_item.quantity >= self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name} in Cart {self.cart.id}"

    class Meta:
        ordering = ['-added_at']
    def checkout(self, shipping_address, phone_number, email):
            if self.completed:
                raise ValidationError("This cart has already been checked out.")

            with transaction.atomic():
                total = self.get_total_price()
                order = Order.objects.create(
                    user=self.user,
                    status='processing',
                    total_amount=total,
                    shipping_address=shipping_address,
                    phone_number=phone_number,
                    email=email
                )

                for item in self.items.select_related('menu_item'):
                    if item.menu_item.quantity < item.quantity:
                        raise ValidationError(f"Not enough stock for {item.menu_item.name}")

                    # Decrease stock
                    item.menu_item.quantity -= item.quantity
                    item.menu_item.save()

                    # Create order item
                    OrderItem.objects.create(
                        order=order,
                        menu_item=item.menu_item,
                        quantity=item.quantity,
                        price=item.menu_item.price
                    )

                self.completed = True
                self.save()

            return order