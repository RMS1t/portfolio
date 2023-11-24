from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from shop.models import Product, Order, OrderItem, Cart, CartItems


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        ReadOnlyField =['id']
        fields= ['id','name','desc','price']

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    total_item = serializers.SerializerMethodField(method_name='get_total_item')

    class Meta:
        model = CartItems  # Передаём модель
        fields = ('id', 'cart', 'product', 'quantity', 'total_item')  # Берем поля из модели + из сериализатора

    # Функция, отвечающая за пересчёт суммы товара, из модели CartItems достаём количество товара и умножаем на его цену
    def get_total_item(self, cart_item=CartItems):
        return cart_item.quantity * cart_item.product.price


# Сериализатор, отвечающий за обработку корзины с товаром, для вывода товаров в корзине используем сериализатор,
# обрабатывающий товары в корзине, дополнительно выводим сумму всей корзины и пользователя, которому принадлежит корзина
class CartSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField(method_name='get_all_total')

    class Meta:
        model = Cart  # Передаем модель Корзины
        fields = ('id', 'user_id', 'items', 'total')  # Берем только поля из сериализатора

    # Функция, отвечающая за пересчёт суммы всей корзины
    def get_all_total(self, cart=Cart):
        items = cart.items.all()
        total = sum([item.quantity * item.product.price for item in
                     items])  # Проходимся циклом по queryset-у Cart, перемножаем количество товара на его цену и
        # суммируем методом sum()
        return total


# Сериализатор, отвечающий за добавление товара в корзину
class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    # Для начала ищем Товар, если не находим выводим исключение, чтобы не возникала ошибка
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('Товар не найден.')

        return value

    # Затем сохраняем объект в корзине
    def save(self, **kwargs):
        cart_id = self.context['cart_id']  # Достаём id корзины из контекста вьюсета
        user = self.context['user']
        product_id = self.validated_data['product_id']  # из validated_data достаём id товара
        quantity = self.validated_data['quantity']  # из validated_data достаём количество товара

        try:
            cart_item = CartItems.objects.get(product_id=product_id,
                                              cart_id=cart_id, user=user)  # С помощью вышеописанных переменных ищем определенные
            # элементы корзины
            cart_item.quantity += quantity  # После того как нашли, добавляем к количеству найденное число,
            # автоматически пересчитывается стоимость
            cart_item.save()  # Сохраняем объект
            self.instance = cart_item  # отдаём как instance(того требует метод)
        except:
            self.instance = CartItems.objects.create(cart_id=cart_id, user=user,
                                                     **self.validated_data)  # Если товара до этого не был добавлен в
            # корзину, то добавляем

        return self.instance  # Возвращаем instance

    class Meta:
        model = CartItems  # Передаем модель Товаров в Корзине
        fields = ('id', 'product_id', 'quantity')  # И поля описанные в модели + поле из сериализатора


# Сериализатор, обновляющий количество определенного товара в корзине
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ('quantity',)


# Сериализатор, отвечающий за вывод предметов в Заказе
class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem  # Передаем модель Товаров в Заказе
        fields = ('id', 'product',
                  'quantity')  # И поля описанные в модели + поле из сериализатора, отвечающее за вывод подробной
        # информации о товарах


# Сериализатор, отвечающий за создание Заказа
class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.IntegerField()  # Передаём id корзины

    def save(self, **kwargs):
        with transaction.atomic():  # Используя SQL транзакции выполняем следующий код
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']  # Из контекста вьюсета получаем id пользователя (владельца корзины/заказа)
            order = Order.objects.create(owner_id=user_id,
                                         status='О')  # Создаём заказ, присваиваем ему пользователя и статус "Оплачен")
            cart_items = CartItems.objects.filter(cart_id=cart_id)  # Находим товары из корзины этого пользователя
            if cart_items.exists():
                order_items = [
                    OrderItem(
                        order=order,
                        product=item.product,
                        quantity=item.quantity)
                    for item in cart_items
                ]  # Проходимся циклом по товарам из корзины пользователя, создаём модель Товаров
                # в Заказе, в качестве владельца передаем пользователя, из корзины передаем информацию о товаре и его количество
                OrderItem.objects.bulk_create(
                    order_items)  # С помощью метода bulk_create в БД записываем полученный выше список
                Cart.objects.filter(user_id=user_id).delete()  # Удаляем корзину пользователя
            else:
                raise serializers.ValidationError('Ваша корзина пуста.')


# Сериализатор, отвечающий за Заказ
class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order  # Передаем модель Заказа
        fields = ('id', 'placed', 'status', 'owner', 'items')
        # И поля описанные в модели + поле из сериализатора, о