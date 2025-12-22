from django.db import models

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100,verbose_name="Имя")
    description = models.TextField(max_length=500, verbose_name='Описание')
    price = models.FloatField()

    def __str__(self):
            return self.name

class Order(models.Model):
    items = models.ManyToManyField(Item)
