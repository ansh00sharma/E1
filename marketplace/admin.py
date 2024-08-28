from django.contrib import admin
from marketplace.models import Cart,Tax

# Register your models here.
class CustomCartAdmin(admin.ModelAdmin):
    list_display = ('user','fooditem','quantity','updated_at') 

class CustomeTaxAdmin(admin.ModelAdmin):
    list_display = ('tax_type','tax_percentage','is_active')
    

admin.site.register(Cart,CustomCartAdmin)
admin.site.register(Tax,CustomeTaxAdmin)
