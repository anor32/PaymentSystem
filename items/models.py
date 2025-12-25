from django.db import models
from django.forms import ModelChoiceField
from django.utils.regex_helper import Choice

from users.models import User


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100,verbose_name="Имя")
    description = models.TextField(max_length=500, verbose_name='Описание')
    price = models.FloatField()
    currency = models.CharField(max_length=4, default='USD',
                                choices=[
                                    ('USD', 'usd'),
                                    ('EUR', 'euro'),
                                    ('RUB', 'rub'),
                                ])
    def __str__(self):
            return self.name

class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)


    @property
    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name + ' '+str(self.quantity)



class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Ожидает оплаты'
        PAID =  'Оплачен'
        SHIPPED = 'Отправлен'
        DELIVERED =  'Доставлен'
        CANCELLED =  'Отменен'


    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)


    @property
    def total_price(self):
        return sum([order_item.total_price for order_item in self.items.all()])


    @property
    def items(self):
        return OrderItem.objects.filter(order=self)
