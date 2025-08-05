from order.models import Order, OrderItem,Cart
from django.db import transaction
from rest_framework.exceptions import PermissionDenied,ValidationError



class OrderService:
    @staticmethod
    def create_order(user_id, cart_id):

        with transaction.atomic():
            cart = Cart.objects.get(pk=cart_id)
            cart_items = cart.items.select_related('product').all()
            
            total_price = sum([item.product.price * item.quantity for item in cart_items])

            order = Order.objects.create(user_id=user_id, total_price=total_price)
            
            order_items = [
                OrderItem(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price,
                    total_price=item.product.price * item.quantity
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)
            
            cart.delete()

            return order
    
    @staticmethod
    def cancel_order(order, user):
        # ✅ First: Check order status before checking permission
        if order.status == Order.CANCELED:
            raise ValidationError({
                "detail": "Order is already canceled."})

        if order.status == Order.DELIVERED:
            raise ValidationError({
                "detail": "Order cannot be canceled after it has been delivered."
            })

        # ✅ Then: Check user permission
        if not (user.is_staff or order.user == user):
            raise PermissionDenied("You do not have permission to cancel this order.")

        # ✅ Proceed with cancellation
        order.status = Order.CANCELED
        order.save()
        return order
