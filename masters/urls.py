from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django.contrib import admin


router = DefaultRouter()
router.register(
    r'vendor_masters',
    views.VendorMastersViewSet,
    basename='VendorMastersViewSet')

router.register(
    r'product_group_masters',
    views.ProductGroupMastersViewSet,
    basename='ProductGroupMastersViewSet')


router.register(
    r'vehicle_type_masters',
    views.VehicleTypeMastersViewSet,
    basename='VehicleTypeMastersViewSet')

urlpatterns = [
        path('', include(router.urls)),  # Include the router's URLs
]