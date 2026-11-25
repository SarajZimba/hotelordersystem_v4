from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework import routers

from ..views.user import CustomTokenObtainPairView, CustomerAPI

from ..views.user import AgentViewSet, AdminViewSet, AdminDeleteAPI, AdminUpdateView


router = routers.DefaultRouter()
router.register('agent-create', AgentViewSet, basename='agent')
router.register('admin-create', AdminViewSet, basename='admin-create')

router.register("customer", CustomerAPI)

urlpatterns = [
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
] + router.urls

urlpatterns += [
    path('admin-delete/', AdminDeleteAPI.as_view(), name='admin-delete'),
    path("admin/update/", AdminUpdateView.as_view(), name="admin-update"),
]
from api.views.user import CustomerDetailAPIView, CustomerListAPIView

urlpatterns += [
    path('customer-detail/<int:pk>/', CustomerDetailAPIView.as_view(), name='customer_detail'),
    path('customer-list/', CustomerListAPIView.as_view(), name='customer_list'),
    # other URL patterns
]