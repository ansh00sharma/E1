from django.contrib import admin
from marketplace.models import Cart

# Register your models here.
class CustomCartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity','updated_at') 


admin.site.register(Cart,CustomCartAdmin)
