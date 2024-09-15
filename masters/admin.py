from django.contrib import admin
from django.db import IntegrityError
from django.shortcuts import redirect, render
from django.urls import path
import pandas as pd
from django.contrib import messages

from django.db import IntegrityError

from masters.models.product_group import ProductGroupMaster, ProductGroupMasterUploadForm
from masters.models.vehicle_type import VehicleTypeMasters
from masters.models.vendor import VendorMasterUploadForm, VendorMasters

# Register your models here.


class VendorMastersAdmin(admin.ModelAdmin):

    change_list_template = "master_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.upload_file, name='masters_vendormasters_upload'),
        ]
        return custom_urls + urls
    
    def upload_file(self, request):
        if request.method == "POST":
            form = VendorMasterUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                df = pd.read_excel(file, engine='openpyxl')
                updated_count = 0
                created_count = 0
                duplicate_names = []
                for _, row in df.iterrows():
                    name = row['VendorMaster']
                    description = row.get('description', None)
                    location = row.get('location', None)
                    email = row.get('description', None)
                    phone = row.get('location', None)
                    s_no = row.get('S.NO', 0)

                    status = True if row.get('Status') == 'L' else False

            # Check if VendorMasters record exists with the same name
                    vendor, created = VendorMasters.objects.get_or_create(
                        name=name,
                        defaults={
                            'description': description,
                            'location': location,
                            'email': email,
                            'phone': phone,
                            'status': status,
                            's_no': s_no
                        }
                    )

                    if not created:
                        # Update existing record
                        vendor.description = description
                        vendor.location = location
                        vendor.email = email
                        vendor.phone = phone
                        vendor.status = status
                        vendor.s_no = s_no
                        vendor.save()
                        updated_count += 1
                    else:
                        created_count += 1

                messages.success(request, f"Vendor masters uploaded: {created_count} created, {updated_count} updated.")
                return redirect('admin:masters_vendormasters_changelist')
        else:
            form = VendorMasterUploadForm()
        return render(request, "master_upload.html", {"form": form})


    list_per_page = 50
    # search_fields = ('branch__branch_name',)
    list_display = [f.name for f in VendorMasters._meta.fields if f.name != 'id' ]
    search_fields = ['name']
    list_filter = ['status']

admin.site.register(VendorMasters, VendorMastersAdmin)



class ProductGroupMasterAdmin(admin.ModelAdmin):
    change_list_template = "master_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.upload_file, name='masters_productgroupmaster_upload'),
        ]
        return custom_urls + urls
    
    def upload_file(self, request):
        if request.method == "POST":
            form = ProductGroupMasterUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                try:
                    df = pd.read_excel(file, engine='openpyxl')
                    updated_count = 0
                    created_count = 0
                    errors = []
                    for index, row in df.iterrows():
                        product = row.get('Product', '')
                        group_code = row['EBomCatName']
                        description = row.get('Description', None)
                        packing_name = row.get('PackingName', '')
                        fixed =  row.get('FixedVariable', 'F')
                        no_of_packages = row.get('NoOfPackages', '')
                        status = True if row.get('Status') == 'L' else False
                        wh_team_name = row.get('WHTeamName', '')
                        source_of_supply = row.get('Source of supply', '')
                        s_no =  row.get('S.No', 0)
                        qr_type = row.get('QR Code generation type', 'Type-1')
                        qr_code_scanning =  row.get('QR Code Scanning', '')
                        use_qr_code_scanning = True if row.get('Flag','N')  == 'Y' else False
                        is_po_mo_mandatory = True if row.get('PO/MO','N')  == 'Y' else False



                        # Check if ProductGroupMaster record exists with the same product and group_code
                        try:
                            obj, created = ProductGroupMaster.objects.update_or_create(
                                product=product,
                                group_code=group_code,
                                defaults={
                                    'description': description,
                                    'packing_name': packing_name,
                                    'fixed': fixed,
                                    'no_of_packages': no_of_packages,
                                    'status': status,
                                    'wh_team_name': wh_team_name,
                                    'source_of_supply': source_of_supply,
                                    's_no':s_no,
                                    'qr_type': qr_type,
                                    'use_qr_code_scanning':use_qr_code_scanning,
                                    'qr_code_scanning':qr_code_scanning,
                                    'is_po_mo_mandatory':is_po_mo_mandatory
                                }
                            )
                            if created:
                                created_count += 1
                            else:
                                updated_count += 1
                            
                            vendor_names = [row.get(f'Supplier-{i}', '').strip() for i in range(1, 6) if isinstance(row.get(f'Supplier-{i}', ''), str)]
                            vendors = []
                            if vendor_names:
                                vendors = VendorMasters.objects.filter(name__in=vendor_names)
                                obj.vendors.set(vendors)
                            
                            if len(vendors) != len(vendor_names):
                                missing_vendors = set(vendor_names) - set(vendors.values_list('name', flat=True))
                                errors.append(f"Row {index + 1}: Missing vendors - {', '.join(missing_vendors)}")
                                continue

                        except IntegrityError as e:
                            messages.error(request, f"Error processing row: {str(e)}")


                    if errors:
                        for error in errors:
                            messages.error(request, error)

                    messages.success(request, f"Product group masters uploaded: {created_count} created, {updated_count} updated.")
                    return redirect('admin:masters_productgroupmaster_changelist')  # Redirect to change list
                
                except Exception as e:
                    messages.error(request, f"Error uploading product group masters: {str(e)}")
                    form.add_error('file', f"Error: {str(e)}")
                    
            else:
                messages.error(request, "Form is not valid. Please check the file.")
        
        else:
            form = ProductGroupMasterUploadForm()
        
        return render(request, "master_upload.html", {"form": form})

    list_per_page = 50
    list_display = [f.name for f in ProductGroupMaster._meta.fields  if f.name != 'id']
    search_fields = ['product', 'group_code', 'description', 'packing_name', 'wh_team_name', 'source_of_supply']
    list_filter = ['status', 'fixed', 'product', 'use_qr_code_scanning', 'is_po_mo_mandatory']


admin.site.register(ProductGroupMaster, ProductGroupMasterAdmin)




class VehicleTypeMastersAdmin(admin.ModelAdmin):

    change_list_template = "master_change_list.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.upload_file, name='masters_vechiletypemasters_upload'),
        ]
        return custom_urls + urls
    
    def upload_file(self, request):
        if request.method == "POST":
            form = VendorMasterUploadForm(request.POST, request.FILES)
            if form.is_valid():
                file = form.cleaned_data['file']
                df = pd.read_excel(file, engine='openpyxl')
                updated_count = 0
                created_count = 0
                for _, row in df.iterrows():
                    vehicleType = row['VehicleType']
                    status = True if row.get('Status') == 'L' else False

            # Check if VendorMasters record exists with the same name
                    vendor, created = VehicleTypeMasters.objects.get_or_create(
                        vechile_type=vehicleType,
                        defaults={
                            'status': status,
                        }
                    )

                    if not created:
                        vendor.status = status
                        vendor.save()
                        updated_count += 1
                    else:
                        created_count += 1

                messages.success(request, f"Vehicle masters uploaded: {created_count} created, {updated_count} updated.")
                return redirect('admin:masters_vehicletypemasters_changelist')
        else:
            form = VendorMasterUploadForm()
        return render(request, "master_upload.html", {"form": form})


    list_per_page = 50
    # search_fields = ('branch__branch_name',)
    list_display = [f.name for f in VehicleTypeMasters._meta.fields if f.name != 'id' ]
    search_fields = ['name']
    list_filter = ['status']

admin.site.register(VehicleTypeMasters, VehicleTypeMastersAdmin)

