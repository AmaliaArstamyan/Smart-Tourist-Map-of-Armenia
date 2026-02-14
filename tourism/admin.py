from django.contrib import admin
from .models import Region, Category, Place

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    search_fields = ['name']

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'region', 'category', 'rating', 'popularity']
    list_filter = ['region', 'category']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'image_url')
        }),
        ('Location', {
            'fields': ('region', 'latitude', 'longitude', 'address')
        }),
        ('Category', {
            'fields': ('category',)
        }),
        ('Contact Information', {
            'fields': ('website', 'phone')
        }),
        ('Visit Details', {
            'fields': ('opening_hours', 'entrance_fee')
        }),
        ('Ratings', {
            'fields': ('rating', 'popularity')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )