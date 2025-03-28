from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .models import SiteMaintenance, UserActivity, UserProfile, HomePageMessage, UserSession
from .serializers import HomePageMessageSerializer, SiteMaintenanceSerializer, UserActivitySerializer, UserSerializer
from rest_framework.permissions import AllowAny
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.utils.timezone import now
from datetime import timedelta

from .serializers import ChangePasswordSerializer
class RegisterAPIView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Create the user
        user = User.objects.create_user(username=username, password=password)
        # Generate a token for the user
        token = Token.objects.create(user=user)
        # Return the token as a response
        return Response({'token': token.key})


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Login the user        
            try:
                if hasattr(user, 'profile') and user.profile.subscription_end < timezone.now().date():
                    return Response({'status': False, 'message': 'Login falied - Your subscription has expired.'})

                if 'admin' not in user.username and 'developer' not in user.username:
                    session = UserSession.objects.filter(user=user, is_active=True, last_activity__gte=(now() - timedelta(minutes=10))).first()
                    if session:
                        return Response({'status':False, 'message': 'User logged-in from another system in the last 10 minutes!'})
            except UserSession.DoesNotExist:
                pass
            
            login(request, user)

            # Check if token exists, delete it if found
            Token.objects.filter(user=user).delete()
            # Create a new token
            token = Token.objects.create(user=user)
            serializer = UserSerializer(user)

            UserSession.objects.update_or_create(
            user=user, 
            defaults={
                'session_key': request.session.session_key,
                'login_time': timezone.now(),
                'is_active': True
            }
        )
            # Return the token as a response
            return Response({'status':True, 
                             'message': 'Credentials Validated',
                             'token': token.key, 
                             'user': serializer.data})
        else:
            return Response({'status':False, 'message': 'Invalid credentials'})


class FetchUserData(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if hasattr(user, 'profile') and user.profile.subscription_end:
            # Calculate days left until the subscription end date
            today = timezone.now().date()
            days_left = (user.profile.subscription_end - today).days

            if days_left < 0:
                return Response({
                    'status': False,
                    'message': "Your subscription has expired."
                })
            elif days_left == 0:
                message = "Today your subscription will be expired."
            elif days_left == 1:
                message = f"Your subscription will expire tomorrow"
            else :
                message = f"Your subscription will expire in {days_left} days"


            user_serializer = UserSerializer(user)

            # Return profile data and days left in response
            return Response({
                'status': True,
                'days_left': days_left,
                'message': message,
                'user_profile': user_serializer.data
            })
        else:
            return Response({
                'status': False,
                'message': "Subscription details not available."
            })

class ProfileUpdateAPIView(APIView):
    def post(self, request):
        user_profile = UserProfile.objects.get(user=request.user)

        # Update the profile fields
        user_profile.location = request.data.get('location')
        user_profile.position = request.data.get('position')
        user_profile.save()

        return Response({'message': 'Profile updated successfully'})

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            user = request.user

            if not check_password(old_password, user.password):
                return Response({
                    'status': False, 
                    'message': 'Old password is incorrect.'}, status=status.HTTP_200_OK)

            user.set_password(new_password)
            user.save()

            return Response({
                'status':True, 
                'message': 'Password changed successfully.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class HomePageMessageViewSet(APIView):
    def get(self, request):
        homepage_message = HomePageMessage.objects.filter(is_active=True).order_by("sequence_no")
        serializer = HomePageMessageSerializer(homepage_message, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

class SiteMaintenanceViewSet(APIView):
    def get(self, request):
        site_maintenance = SiteMaintenance.objects.filter(under_maintenance=True).order_by("-updated_at").first()
        serializer = SiteMaintenanceSerializer(site_maintenance)
        return Response(serializer.data, status.HTTP_200_OK)

from rest_framework import viewsets

class UserActivityViewSet(APIView):
    queryset = UserActivity.objects.all()
    serializer_class = UserActivitySerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        
        serializer = UserActivitySerializer(data=request.data)
        user_profile = UserProfile.objects.get(user=request.user)
        if request.data.get('type') == 'Login':
            user_profile.is_logged_in = True
        else:
            user_profile.is_logged_in = False 
            try:
                session = session = UserSession.objects.get(user=request.user, is_active=True)
                session.is_active = False
                session.save()
            except UserSession.DoesNotExist:
                pass    
        user_profile.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)