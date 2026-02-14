from django.db import models

class Region(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, blank=True, help_text="FontAwesome or emoji icon")
    
    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='places')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='places')
    address = models.CharField(max_length=300, blank=True)
    website = models.URLField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    opening_hours = models.CharField(max_length=200, blank=True)
    entrance_fee = models.CharField(max_length=100, blank=True)
    rating = models.FloatField(default=0)
    popularity = models.IntegerField(default=0, help_text="Number of visits/reviews")
    image_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-popularity', 'name']