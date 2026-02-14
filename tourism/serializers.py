from rest_framework import serializers
from .models import Region, Category, Place

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ['id', 'name', 'description']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class PlaceSerializer(serializers.ModelSerializer):
    region_name = serializers.CharField(source='region.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_icon = serializers.CharField(source='category.icon', read_only=True)
    
    class Meta:
        model = Place
        fields = ['id', 'name', 'description', 'latitude', 'longitude', 
                  'region', 'region_name', 'category', 'category_name', 
                  'category_icon', 'address', 'website', 'phone', 
                  'opening_hours', 'entrance_fee', 'rating', 'popularity', 
                  'image_url']