from django.contrib import admin
from menu.models import Category, FoodItem

# Register your models here.
class CustomCategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name','vendor','updated_at',)
    search_fields = ('category_name','vendor__vendor_name')
    

class CustomFoodItemAdmin(admin.ModelAdmin):
    def category_name(self, obj):
        return obj.category.category_name
        
    prepopulated_fields = {'slug': ('food_title',)}
    list_display = ('food_title','category_name','vendor','price','is_available','updated_at')
    search_fields = ('food_title','category_name','vendor__vendor_name','price')
    list_filter = ('is_available',)

admin.site.register(Category,CustomCategoryAdmin)
admin.site.register(FoodItem,CustomFoodItemAdmin)
