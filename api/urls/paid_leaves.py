from django.urls import path
from api.views.paid_leaves import tblcompanypaidleavePolicyCreateAPIView,tblleaveapplyCreateAPIView, GetEmploeeNoofPaidLeavesApiView, tblleaveapplyListAPIView, tblleaveapplyUpdateAPIView, tblleaveapplyCancelAPIView, GetEmployeePaidLeaves, tblleaveapplyDeleteAPIView, tblleaveapplyEmployeeCreateAPIView, tblleaveapplyStatusUpdateAPIView



urlpatterns = [
    path('paid-leave-policy/', tblcompanypaidleavePolicyCreateAPIView.as_view(), name='paid-leave-policy'),
    path('leave-apply/', tblleaveapplyCreateAPIView.as_view(), name='leave-apply'),
    path('employee/leave-apply/', tblleaveapplyEmployeeCreateAPIView.as_view(), name='emploee-leave-apply'),

    path('get-leave-apply/', tblleaveapplyListAPIView.as_view(), name='get-leave-apply'),
    path('get-employee-paidleaves/', GetEmploeeNoofPaidLeavesApiView.as_view(), name='get-employee-paidleaves'),
    path('cancel-tbleaveapply/', tblleaveapplyCancelAPIView.as_view(), name='cancel-tbleaveapply'),
    path('get-paid-leaves/', GetEmployeePaidLeaves.as_view(), name='get-paid-leaves'),

]

urlpatterns += [
path("leave-apply/<int:pk>/update/", tblleaveapplyUpdateAPIView.as_view()),
path("leave-apply/<int:pk>/delete/", tblleaveapplyDeleteAPIView.as_view()),
path("leave-apply-status/<int:pk>/update/", tblleaveapplyStatusUpdateAPIView.as_view()),


]