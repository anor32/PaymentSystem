from django.db import models
from users.models import User


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    description = models.TextField(max_length=500, verbose_name='Описание')
    price = models.FloatField()


    def __str__(self):
        return self.name


class OrderItem(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_items')
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.IntegerField(default=1)
    currency = models.CharField(max_length=4, default='USD',
                                choices=[
                                    ('USD', 'usd'),
                                    ('EUR', 'euro'),
                                ])
    @property
    def total_price(self):
        return self.item.price * self.quantity

    def __str__(self):
        return self.item.name + ' ' + str(self.quantity)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'Ожидает оплаты'
        PAID = 'Оплачен'
        SHIPPED = 'Отправлен'
        DELIVERED = 'Доставлен'
        CANCELLED = 'Отменен'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    tax = models.ForeignKey('Tax', on_delete=models.PROTECT, null=True, blank=True)
    discount = models.ForeignKey('Discount', on_delete=models.PROTECT, null=True, blank=True)

    @property
    def total_price(self):
        items_sum = sum([order_item.total_price for order_item in self.items.all()])
        total_price = items_sum
        if self.discount:
            total_price -= total_price * self.discount.percent / 100

        if self.tax:
            total_price += total_price * self.tax.percent / 100

        return total_price

    @property
    def items(self):
        return OrderItem.objects.filter(order=self)

    def __str__(self):
        return str(self.pk)


class Discount(models.Model):
    name = models.CharField(max_length=100, blank=True)
    percent = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.percent}%)"


class Tax(models.Model):
    name = models.CharField(max_length=100, blank=True)
    percent = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.percent}%)"