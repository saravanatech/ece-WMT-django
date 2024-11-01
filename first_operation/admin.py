from django.contrib import admin
from django.urls import path
from django.shortcuts import render, redirect
from django.contrib import messages
import pandas as pd

from first_operation.models.batch import Batch
from first_operation.models.batch_items import BatchItems
from first_operation.models.batch_nesting_items import BatchNestingItems
from first_operation.models.item_type_master import ItemTypeMaster, ItemTypeMasterMasterUploadForm
from first_operation.models.rm_code_master import RMCodeMasterMasterUploadForm
from .models import RMCodeMaster

class RMCodeMasterAdmin(admin.ModelAdmin):

    change_list_template = "master_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.upload_file, name='masters_rmcode_upload'),
        ]
        return custom_urls + urls

    def upload_file(self, request):
        if request.method == "POST":
            form = RMCodeMasterMasterUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                df = pd.read_excel(file, engine='openpyxl')
                updated_count = 0
                created_count = 0
                for _, row in df.iterrows():
                    s_no = row.get('S No', 0)
                    rm_code = row['RM Code']
                    description = row.get('Description')
                    sheet_thickness = row.get('Sheet Thickness')
                    material = row.get('Material')
                    status = True if row.get('Status') == 'L' else False
                    

                    # Check if RMCodeMaster record exists with the same rm_code and sheet_thickness
                    rmcode, created = RMCodeMaster.objects.get_or_create(
                        rm_code=rm_code,
                        sheet_thickness=sheet_thickness,
                        defaults={
                            's_no': s_no,
                            'description': description,
                            'material': material,
                            'status': status
                        }
                    )

                    if not created:
                        # Update the existing record
                        rmcode.description = description
                        rmcode.material = material
                        rmcode.status = status
                        rmcode.s_no = s_no
                        rmcode.save()
                        updated_count += 1
                    else:
                        created_count += 1

                messages.success(request, f"RM Code Masters uploaded: {created_count} created, {updated_count} updated.")
                return redirect('admin:first_operation_rmcodemaster_changelist')
        else:
            form = RMCodeMasterMasterUploadForm()
        return render(request, "master_upload.html", {"form": form})

    list_per_page = 50
    list_display = [f.name for f in RMCodeMaster._meta.fields if f.name != 'id']
    search_fields = ['rm_code', 'description']
    list_filter = ['sheet_thickness', 'status']

admin.site.register(RMCodeMaster, RMCodeMasterAdmin)




class ItemTypeMasterAdmin(admin.ModelAdmin):

    change_list_template = "master_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.upload_file, name='masters_itemtypemaster_upload'),
        ]
        return custom_urls + urls

    def upload_file(self, request):
        if request.method == "POST":
            form = ItemTypeMasterMasterUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                df = pd.read_excel(file, engine='openpyxl')
                updated_count = 0
                created_count = 0
                for _, row in df.iterrows():
                    s_no = row.get('S No', 0)
                    item_code = row['Item Code']
                    item_type = row.get('Type')
                    status = True if row.get('Status') == 'L' else False

                    # Check if ItemTypeMaster record exists with the same item_code
                    item, created = ItemTypeMaster.objects.get_or_create(
                        item_code=item_code,
                        defaults={
                            's_no': s_no,
                            'type': item_type,
                            'status': status,
                        }
                    )

                    if not created:
                        # Update the existing record
                        item.s_no = s_no
                        item.type = item_type
                        item.status = status
                        item.save()
                        updated_count += 1
                    else:
                        created_count += 1

                messages.success(request, f"ItemTypeMaster uploaded: {created_count} created, {updated_count} updated.")
                return redirect('admin:first_operation_itemtypemaster_changelist')
        else:
            form = ItemTypeMasterMasterUploadForm()
        return render(request, "master_upload.html", {"form": form})

    list_per_page = 50
    list_display = [f.name for f in ItemTypeMaster._meta.fields if f.name != 'id']
    search_fields = ['item_code', 'type']
    list_filter = ['status']

admin.site.register(ItemTypeMaster, ItemTypeMasterAdmin)



class BatchAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in Batch._meta.fields]
    search_fields = ['batch_no']
    list_filter = ['status']

admin.site.register(Batch, BatchAdmin)


class BatchItemsAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in BatchItems._meta.fields]
    search_fields = ['batch__batch_no', 'material', 'rm_code', 'description']
    list_filter = ['status', 'error']

admin.site.register(BatchItems, BatchItemsAdmin)


class BatchNestingItemsAdmin(admin.ModelAdmin):
    list_per_page = 50
    list_display = [f.name for f in BatchNestingItems._meta.fields]
    search_fields = ['batch_items__batch__batch_no', 'nesting_item_code', 'batch_items__rm_code', 'batch_items__description']
    list_filter = ['status']

admin.site.register(BatchNestingItems, BatchNestingItemsAdmin)