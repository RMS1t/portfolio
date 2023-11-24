"""
URL configuration for simplebuy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_nested import routers
from shop.views import ProductViewSet, CartViewSet, OrderViewSet, CartItemViewSet

router = routers.SimpleRouter()  # Создаем роутер для вьюсетов
router.register(r'products', ProductViewSet)  # Регистрируем вьюсет, отвечающий за продукты
router.register(r'carts', CartViewSet)  # Регистрируем вьюсет, отвечающий за корзину
router.register(r'orders', OrderViewSet, basename='orders')  # Регистрируем вьюсет, отвечающий за заказ

cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet,
                     basename='cart-items')  # Регистрируем вьюсет, отвечающий за товары в корзине

urlpatterns = [

    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('', include(router.urls)),
    path('', include(cart_router.urls)),

]

