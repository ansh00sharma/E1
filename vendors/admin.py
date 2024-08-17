from django.contrib import admin
from vendors.models import Vendor
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomVendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','is_approved','created_at')
    # list_display_links = ('user','vendor_name')
    


admin.site.register(Vendor, CustomVendorAdmin)