from django.db import models
from django import forms

class ProductGroupPackageMaster(models.Model):
    product = models.CharField(max_length=100, db_index=True)
    group_code = models.CharField(max_length=100, db_index=True)     
    qty = models.IntegerField(default=1) 
    no_of_packages = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('product', 'group_code','qty')

    def __str__(self):  # __unicode__ on Python 2
        return str(self.group_code)
    


class ProductGroupPackageMasterUploadForm(forms.Form):
    file = forms.FileField()