from django.contrib import admin

from items.models import Item, Order, OrderItem


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id','order_items','total_price','user')



    def order_items(self, obj):
        result_string = ''
        for item in obj.items.all():
            result_string +=   item.item.name + '  '+ str(item.quantity) + 'шт '

        return result_string



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id','item','quantity')

