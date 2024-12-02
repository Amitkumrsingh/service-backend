from django.contrib import admin
from .models import Vehicle, Component, ServiceIssue
@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'owner_name', 'owner_contact')
    search_fields = ('license_plate', 'owner_name')

@admin.register(Component)
class ComponentAdmin(admin.ModelAdmin):
    list_display = ('name', 'repair_price', 'new_price', 'stock')
    search_fields = ('name',)

@admin.register(ServiceIssue)
class ServiceIssueAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'component', 'is_repair', 'description', 'cost', 'created_at')
    list_filter = ('is_repair', 'created_at')
    search_fields = ('vehicle__license_plate', 'description')

