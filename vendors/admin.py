from django.contrib import admin
from vendors.models import Vendor, OpeningHour
from django.contrib.auth.admin import UserAdmin

# Register your models here.
class CustomVendorAdmin(admin.ModelAdmin):
    list_display = ('user','vendor_name','is_approved','created_at')
    # list_display_links = ('user','vendor_name')
    list_editable = ('is_approved',)    

class CustomOpeningHourAdmin(admin.ModelAdmin):
    list_display = ('vendor','day','from_hour','to_hour')


admin.site.register(Vendor, CustomVendorAdmin)
admin.site.register(OpeningHour,CustomOpeningHourAdmin)