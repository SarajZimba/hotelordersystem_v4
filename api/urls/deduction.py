from django.urls import path
from api.views.deduction import DeductionCreateView, MasterDeductionListCreateAPIView, MasterDeductionDetailAPIView, EmployeeDeductionListCreateAPIView, EmployeeDeductionDetailAPIView

urlpatterns = [
    path('deductions/', DeductionCreateView.as_view(), name='deduction-create'),

    path('masterdeduction/', MasterDeductionListCreateAPIView.as_view(), name='masterdeduction-list-create'),
    path('masterdeduction/<int:pk>/', MasterDeductionDetailAPIView.as_view(), name='masterdeduction-detail'),

    path('employeededuction/', EmployeeDeductionListCreateAPIView.as_view(), name='employeededuction-list-create'),
    path('employeededuction/<int:pk>/', EmployeeDeductionDetailAPIView.as_view(), name='employeededuction-detail'),
]


