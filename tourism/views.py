from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from django.db.models import Q
import random

from .models import Region, Category, Place
from .serializers import RegionSerializer, CategorySerializer, PlaceSerializer

class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class PlaceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['region', 'category']

def map_view(request):
    return render(request, 'tourism/map.html')

@api_view(['POST'])
def plan_trip(request):
    data = request.data
    days = int(data.get('days', 2))
    budget = data.get('budget', 'medium')
    interests = data.get('interests', [])
    transport = data.get('transport', 'car')
    
    # Filter places based on interests
    places = Place.objects.all()
    if interests:
        # Handle multiple interest categories
        category_filter = Q()
        for interest in interests:
            category_filter |= Q(category__name__icontains=interest)
        places = places.filter(category_filter)
    
    # Sort by popularity (recommendation logic)
    places = places.order_by('-popularity', 'rating')
    
    # Group places by region for efficient routing
    places_by_region = {}
    for place in places:
        region_name = place.region.name
        if region_name not in places_by_region:
            places_by_region[region_name] = []
        places_by_region[region_name].append(place)
    
    # Generate daily itinerary
    trip_plan = []
    all_places = list(places)
    random.shuffle(all_places)  # Add some variety
    
    places_per_day = max(1, len(all_places) // days)
    
    for day in range(days):
        start_idx = day * places_per_day
        end_idx = start_idx + places_per_day if day < days - 1 else len(all_places)
        day_places = all_places[start_idx:end_idx]
        
        day_plan = {
            'day': day + 1,
            'places': [],
            'total_distance': random.randint(20, 150),  # Mock distance
            'estimated_time': f"{len(day_places) * 1.5} hours",
            'budget_estimate': calculate_budget(budget, len(day_places))
        }
        
        for place in day_places:
            day_plan['places'].append({
                'id': place.id,
                'name': place.name,
                'category': place.category.name,
                'region': place.region.name,
                'rating': place.rating,
                'entrance_fee': place.entrance_fee,
                'image_url': place.image_url,
                'description': place.description[:100] + '...' if len(place.description) > 100 else place.description
            })
        
        trip_plan.append(day_plan)
    
    return Response({
        'trip_plan': trip_plan,
        'summary': {
            'total_days': days,
            'total_places': len(all_places),
            'budget_level': budget,
            'interests': interests
        }
    })

def calculate_budget(budget_level, num_places):
    base_costs = {
        'low': 50,
        'medium': 150,
        'high': 300
    }
    return base_costs.get(budget_level, 100) * num_places

@api_view(['GET'])
def get_trip_suggestions(request):
    """Get quick trip suggestions based on duration"""
    duration = request.GET.get('duration', 'weekend')
    
    suggestions = {
        'weekend': [
            {'name': 'Yerevan City Tour', 'places': ['Republic Square', 'Cascade', 'Matenadaran']},
            {'name': 'Garni & Geghard', 'places': ['Garni Temple', 'Geghard Monastery', 'Charents Arch']}
        ],
        '3days': [
            {'name': 'Classic Armenia', 'places': ['Yerevan', 'Garni', 'Geghard', 'Sevan']},
            {'name': 'Northern Adventure', 'places': ['Dilijan', 'Haghartsin', 'Goshavank']}
        ],
        'week': [
            {'name': 'Complete Armenia', 'places': ['Yerevan', 'Garni', 'Geghard', 'Sevan', 'Dilijan', 'Tatev']}
        ]
    }
    
    return Response(suggestions.get(duration, suggestions['weekend']))



def test_page(request):
    return render(request, 'tourism/test.html')