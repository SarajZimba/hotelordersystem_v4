from django.urls import path
from api.views.organization import OrganizationApi, BranchApi, PrinterSettingListView,TestMaster,BranchCreateAPIView,BranchDetailAPIView
from rest_framework import routers

router = routers.DefaultRouter()

router.register("organization", OrganizationApi)
router.register("branch", BranchApi)

urlpatterns = [
    path('printer-setting/<int:branch_id>/<int:terminal_no>', PrinterSettingListView.as_view(), name='printer-setting'),
    path('test-master', TestMaster.as_view(), name='test-master'),
    path("branch/create/", BranchCreateAPIView.as_view(), name="branch-create"),
    path("branch/<int:pk>/manage/", BranchDetailAPIView.as_view(), name="branch-manage"),
    ] + router.urls

from django.urls import path
from api.views.organization import TrialBalanceToggleAPIView

urlpatterns += [
    path('trialbalance/toggle/', TrialBalanceToggleAPIView.as_view(), name='trialbalance-toggle'),
]