from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from masters.models.vendor import VendorMasters


class Branch(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ScreenAccess(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    is_logged_in = models.BooleanField(default=False)
    subscription_start = models.DateField()
    subscription_end = models.DateField()
    screens = models.ManyToManyField(ScreenAccess, blank=True, related_name='screens')  # Add this field to represent the relationship  
    vendor = models.ManyToManyField(VendorMasters, blank=True, related_name='vendor_masters')  # Add this field to represent the relationship  

    def save(self, *args, **kwargs):
        if not self.pk and not self.user_id:
            super(UserProfile, self).save(*args, **kwargs)
            self.user.profile = self
            self.user.save()
        else:
            super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    


class HomePageMessage(models.Model):
    message = models.CharField(max_length=500)
    created_by =  models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    sequence_no = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message


class SiteMaintenance(models.Model):
    message = models.CharField(max_length=500)
    under_maintenance = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)   

    def __str__(self):
        return self.message


class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    activity = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.activity}'


class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=255, unique=True)
    login_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.session_key}"