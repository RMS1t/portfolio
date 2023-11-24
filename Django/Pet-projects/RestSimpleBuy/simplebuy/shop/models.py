from django.db import models
from  simplebuy import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='cart-owner')

    def __str__(self):
        return str(self.id)


# Модель Товаров в Корзине с тремя обязательными полями(в какой корзине лежат товары, какие товары и в каком количестве)
class CartItems(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='cart')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitems', verbose_name='item')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='item_owner')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='items_quantity')



class Order(models.Model):
    STATUS_CHOICES = [
        ('P', 'Paid'),
        ('C', 'Completed'),
        ('F', 'Failed')
    ]

    placed = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время оформления')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, verbose_name='Статус заказа')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, verbose_name='Владелец')

    def __str__(self):
        return self.status


# Модель Товаров в Заказе с тремя обязательными полями(что за заказ, какие товары и в каком количестве)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items', verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=0, verbose_name='Количество')

    def __str__(self):
        return self.product.name