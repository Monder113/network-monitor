# switch/admin.py
from django.contrib import admin
from .models import Switch, Vendor, DeviceModel, PingHistory

@admin.register(Switch)
class SwitchAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'vendor', 'model', 'status', 'last_seen')
    list_filter = ('status', 'vendor')

    class Media:
        js = ("admin/js/vendor_model_filter.js",)  # JS ile dinamik filtreleme

@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DeviceModel)
class DeviceModelAdmin(admin.ModelAdmin):
    list_display = ('vendor', 'name')
    list_filter = ('vendor',)
    search_fields = ('name',)

@admin.register(PingHistory)
class PingHistoryAdmin(admin.ModelAdmin):
    list_display = ('switch', 'timestamp', 'is_reachable', 'response_time')
    list_filter = ('switch', 'is_reachable')
