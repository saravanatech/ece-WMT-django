from django.db import models
from django import forms

class VendorMasters(models.Model):
    s_no = models.IntegerField(default=0)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.CharField(max_length=255, blank=False, null=True)     
    location = models.CharField(max_length=255, blank=False, null=True) 
    email = models.EmailField(max_length=255, blank=False, null=True)
    phone = models.CharField(max_length=255, blank=False, null=True) 
    status = models.BooleanField(default='False', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return str(self.name)
    


class VendorMasterUploadForm(forms.Form):
    file = forms.FileField()