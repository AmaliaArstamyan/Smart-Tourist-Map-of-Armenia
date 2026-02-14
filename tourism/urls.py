from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegionViewSet, CategoryViewSet, PlaceViewSet, map_view, plan_trip, get_trip_suggestions, test_page

router = DefaultRouter()
router.register(r'regions', RegionViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'places', PlaceViewSet)

urlpatterns = [
    path('map/', map_view, name='map'),
    path('plan_trip/', plan_trip, name='plan_trip'),
    path('trip_suggestions/', get_trip_suggestions, name='trip_suggestions'),
    path('', include(router.urls)),
    path('test/', test_page, name='test_page'),  # Changed from views.test_page to test_page
]