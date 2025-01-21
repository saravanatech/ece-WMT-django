from django.urls import path

from project.views.activity_log import ActivityLogCreateView
from project.views.part import BulkPartUpdateView, FetchRejectedPartsView, GoodsQCFailed, GoodsRecieved, MovePartToApprovedrView, MovePartToDoneView, MovePartToVendorView, PartECNtUpdateView, PartPackageAllocationView, PartPackingSlipGeneratedView, PartQRGeneratedView, PartVehicleLoadingUpdateView, PartsForAcceptance, PartsForAcceptanceResponse, ScannedWhileLoadingView, ScannedWhileUnLoading, VendorAcceptedPartsView, VendorRejectedPartsView, VendorStatsView
from project.views.part_log import PartLogListByPartID, PartLogListByProjectID
from project.views.project import ProjectListFilterPagenatedView, ProjectListFilterPartStatusAndProjectIdView, ProjectListFilterPartStatusView, ProjectListFilterStatusPagenatedView, ProjectListFilterView, ProjectListMRDFilterPagenatedView, ProjectListView, ProjectNewlyAddedVendorSummaryView, ProjectSummaryFilterView, ProjectSummaryView, ProjectVendorSummaryFilterView, ProjectVendorSummaryView
from project.views.vehicle import ActiveDistributionCenterVehicleListView, ActiveVehicleListView, BayTimeView, CancelVehicle, Recent30VehicleListView, ShippedVehicle, VehicleCreateView, VehicleDetailView, VehicleListView, VehicleUpdateView

from .views import EbomUploadView, ProjectView

urlpatterns = [
    path('ebom/upload/', EbomUploadView.as_view(), name='ebom-upload'),
    path('list/', ProjectListView.as_view(), name='project-list'),
    path('list/filter/', ProjectListFilterPagenatedView.as_view(), name='project-filter-list'),

    
    path('list/part_status/', ProjectListFilterPartStatusView.as_view(), name='project-status-list'),
    path('list/part_status_projects/', ProjectListFilterStatusPagenatedView.as_view(), name='project-status-list-pagenated'),
    path('list/part_for_project_ids/', ProjectListFilterPartStatusAndProjectIdView.as_view(), name='parts for project ids'),
    path('part-for-acceptance/', PartsForAcceptance.as_view(), name='parts-accptance'),
    path('partsForAcceptanceResponse', PartsForAcceptanceResponse.as_view(), name='partsForAcceptanceResponse'),
    path('vendor-stats/', VendorStatsView.as_view(), name='vendor-stats'),
    path('summary-tracker/', ProjectSummaryView.as_view(), name='project-Summary-view'),
    path('summary-tracker/filter/', ProjectSummaryFilterView.as_view(), name='project-Summary-filter'),
    path('summary-tracker/mrd_filter/', ProjectListMRDFilterPagenatedView.as_view(), name='project-mrd-filter-list'),
    path('vendor-summary-tracker/', ProjectVendorSummaryView.as_view(), name='project-vendor-Summary-view'),
    path('vendor-summary-tracker/filter/', ProjectVendorSummaryFilterView.as_view(), name='project-vendor-Summary-filter'),
    path('vendor-summary-tracker/new/', ProjectNewlyAddedVendorSummaryView.as_view(), name='project-new-vendor-Summary-filter'),
    path('detail/', ProjectView.as_view(), name='project-fetch'),
    path('isValid/', ProjectView.as_view(), name='project-valid'),
    path('parts/bulk-update/', BulkPartUpdateView.as_view(), name='bulk-part-update'),
    path('parts/ecn-update/', PartECNtUpdateView.as_view(), name='ecn-update'),
    path('parts/vehicle-update/', PartVehicleLoadingUpdateView.as_view(), name='ecn-update'),
    path('parts/move-to-vendor/', MovePartToVendorView.as_view(), name='move-to-vendor'),
    path('parts/move-to-approved/', MovePartToApprovedrView.as_view(), name='move-to-approved'),
    path('parts/move-to-done/', MovePartToDoneView.as_view(), name='move-to-done'),
    path('parts/vendor-accpeted/', VendorAcceptedPartsView.as_view(), name='vendor-accpeted'),
    path('parts/vendor-rejected/', VendorRejectedPartsView.as_view(), name='vendor-rejected'),

    path('parts/rejection-list/', FetchRejectedPartsView.as_view(), name='fetch-rejection-list'),
    
    path('parts/qr-generated/', PartQRGeneratedView.as_view(), name='move-to-qr-generated'),
    path('parts/scanned_while_loading/', ScannedWhileLoadingView.as_view(), name='scanned_while_loading'),
    path('parts/scanned_while_un_loading/', ScannedWhileUnLoading.as_view(), name='scanned_while_un_loading'), 
    path('parts/package-allocation-done/', PartPackageAllocationView.as_view(), name='move-to-package-allocation-done'),  
    path('parts/packing-slip-generated/', PartPackingSlipGeneratedView.as_view(), name='packing-slip-generated'),   
    path('partlogs/<int:part_id>/', PartLogListByPartID.as_view(), name='partlog-list-by-part-id'),
    path('projectlogs/<int:project_id>/', PartLogListByProjectID.as_view(), name='partlog-list-by-project-id'),
    path('activity-logs/', ActivityLogCreateView.as_view(), name='activity-log-create'),
    
    path('vehicles/create/', VehicleCreateView.as_view(), name='create_vehicle'),
    path('vehicles/active/', ActiveVehicleListView.as_view(), name='active_vehicles'),
    path('vehicles/dc_active/', ActiveDistributionCenterVehicleListView.as_view(), name='distibution_active_vehicles'),
    path('vehicles/update/<int:pk>/', VehicleUpdateView.as_view(), name='update_vehicle'),
    path('vehicles/detail/', VehicleDetailView.as_view(), name='vehicle_details'),
    path('vehicles/compute_bay_timing/', BayTimeView.as_view(), name='vehicle_by_details'),
    path('vehicles/cancel/', CancelVehicle.as_view(), name='cancel_vehicle'),
    path('vehicles/shipped/', ShippedVehicle.as_view(), name='shipped_vehicle'),
    path('vehicles/recent30/', Recent30VehicleListView.as_view(), name='shipped_vehicle'),
    path('vehicles/list/', VehicleListView.as_view(), name='vehicle_list'),

    path('goods_receipt/received/', GoodsRecieved.as_view(), name='goods-receipt-recieved'),
    path('goods_receipt/qc_failed/', GoodsQCFailed.as_view(), name='goods-receipt-qc-failed')

]
