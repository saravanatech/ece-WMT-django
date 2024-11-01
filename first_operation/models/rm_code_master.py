from django.db import models
from django import forms

class RMCodeMaster(models.Model):
    s_no = models.IntegerField(default=0)
    rm_code = models.CharField(max_length=100, db_index=True)
    description = models.CharField(max_length=255, blank=False, null=True) 
    sheet_thickness =  models.CharField(max_length=10)
    material = models.CharField(max_length=255)
    status = models.BooleanField(default='False', db_index=True)
    
    class Meta:
        unique_together = ('rm_code', 'sheet_thickness')

    def __str__(self):  # __unicode__ on Python 2
        return str(self.rm_code)
    


class RMCodeMasterMasterUploadForm(forms.Form):
    file = forms.FileField()