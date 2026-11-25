from ..views.salary_journal_entry import LiquidAssetLedgersForPaymentAPIView
from django.urls import path

urlpatterns = [
    path("liquidassetledgers/", LiquidAssetLedgersForPaymentAPIView.as_view(), name="liquidassetledgers"),
]