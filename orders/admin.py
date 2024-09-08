from django.contrib import admin
from .models import Payment, Order, OrderedFood

# Register your models here.

class customeOrderedFood(admin.TabularInline):
    model = OrderedFood
    readonly_fields = ('order','payment','user','fooditem','quantity','price','amount')
    extra = 0


class customeOrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','name','phone','email','total','payment_method','status','is_ordered']
    inlines = [customeOrderedFood]

admin.site.register(Payment)
admin.site.register(Order,customeOrderAdmin)
admin.site.register(OrderedFood)