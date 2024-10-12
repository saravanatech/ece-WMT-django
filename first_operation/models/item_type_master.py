from django.db import models
from django import forms

class ItemTypeMaster(models.Model):
    s_no = models.IntegerField(default=0)
    item_code = models.CharField(max_length=100, db_index=True, unique=True)
    type = models.CharField(max_length=50, blank=False, null=True) 
    status = models.BooleanField(default='False', db_index=True)

    def __str__(self):  # __unicode__ on Python 2
        return str(self.item_code + ' - ' + self.type)

class ItemTypeMasterMasterUploadForm(forms.Form):
    file = forms.FileField()