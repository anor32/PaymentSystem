from django.contrib import admin

from items.models import Item, Order


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity', 'price')