from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from .models import HomePageMessage, SiteMaintenance, UserActivity, UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    branches = serializers.StringRelatedField(many=True)
    screens = serializers.StringRelatedField(many=True)
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)
        return user


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class HomePageMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomePageMessage
        fields = '__all__'


class SiteMaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteMaintenance
        fields = '__all__'


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = '__all__'