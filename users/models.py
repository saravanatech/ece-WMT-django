from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
    is_sales = models.BooleanField(default=False)
    is_sales_manager = models.BooleanField(default=False,help_text=
                                           "Note: If this is enabled, is Sales will be enabled automatically")
    is_ho = models.BooleanField(default=False)
    is_dmd = models.BooleanField(default=False)
    is_nib = models.BooleanField(default=False)
    can_archieve = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)
    branches = models.ManyToManyField(Branch, blank=True, related_name='branches')  # Add this field to represent the relationship
    screens = models.ManyToManyField(ScreenAccess, blank=True, related_name='screens')  # Add this field to represent the relationship
    
    def validate_mandatory_fields(self):
        if self.is_sales_manager and not self.is_sales:
            self.is_sales = True
        if not any([self.is_sales, self.is_ho, self.is_dmd, self.is_nib]):
            raise ValidationError(_("At least one of is_sales, is_ho, is_dmd, or is_nib must be True."))
        

    def save(self, *args, **kwargs):
        self.validate_mandatory_fields()

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


