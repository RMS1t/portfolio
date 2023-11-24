from django.contrib import admin

from .models import OrderPetition, Category, AdvUser

# Register your models here.
admin.site.register(OrderPetition)
admin.site.register(Category)
admin.site.register(AdvUser)