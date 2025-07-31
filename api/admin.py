from django.contrib import admin
from order.models import Cart, CartItem
# Register your models here.
admin.site.register(CartItem)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username',)
    list_filter = ('created_at',)
