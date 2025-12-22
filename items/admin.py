from django.contrib import admin

from items.models import Item


# Register your models here.
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','price')
