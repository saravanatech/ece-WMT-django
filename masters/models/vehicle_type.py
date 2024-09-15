from django.db import models
from django import forms

class VehicleTypeMasters(models.Model):
    vechile_type = models.CharField(max_length=100, unique=True, db_index=True)
    status = models.BooleanField(default='False', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):  # __unicode__ on Python 2
        return str(self.vechile_type)

class VechileLoadingMasterUploadForm(forms.Form):
    file = forms.FileField()