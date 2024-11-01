from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import FetchUserData, UserActivityViewSet
from .views import ChangePasswordView, HomePageMessageViewSet, RegisterAPIView, LoginAPIView, ProfileUpdateAPIView, SiteMaintenanceViewSet


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('fetch_user_data/', FetchUserData.as_view(), name='fetch-user-data'),
    path('profile/update/', ProfileUpdateAPIView.as_view(), name='api-profile-update'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('home-page-message/', HomePageMessageViewSet.as_view(), name='home_pageMessage'),
    path('site_maintenance/', SiteMaintenanceViewSet.as_view(), name='site_maintenance'),
    path('user-activity/', UserActivityViewSet.as_view(), name='useractivity')
]
