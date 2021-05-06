from django.conf import settings
from django.db import models

from mainapp.models import Product

# class BasketQuerySet(models.QuerySet):                            #Менеджер объектов
#     def delete(self):
#         for item in self:
#             item.product.quantity += item.quantity
#             item.product.save()
#         super().delete()

class Basket(models.Model):
    # objects = BasketQuerySet.as_manager()                       #Менеджер объектов

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)
    add_datetime = models.DateTimeField(auto_now_add=True, verbose_name='время')

    @property
    def product_const(self):
        return self.product.price * self.quantity

    @property
    def total_quantity(self):
        _items = Basket.objects.filter(user=self.user)
        _total_quantity = sum(list(map(lambda x: x.quantity, _items)))
        return _total_quantity

    @property
    def total_cost(self):
        _items = Basket.objects.filter(user=self.user)
        _total_cost = sum(list(map(lambda x: x.product_const, _items)))
        return _total_cost

    @staticmethod
    def get_item(pk):
        #Basket.objects.get(pk=pk)
        return Basket.objects.filter(user=pk)


    # def delete(self):                                             #Менеджер объектов
    #     self.product.quantity += self.quantity
    #     self.product.save()
    #     super().delete()