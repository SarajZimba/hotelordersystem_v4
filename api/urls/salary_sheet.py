from django.urls import path
from api.views.salary_sheet import EmployeeSalarySheetAPIView, EmployeeYearlySalarySheetAPIView, BranchSalarySheetAPIView, SaveMonthlySalaryReportAPIView, MonthlySalaryReportDetailAPIView, MonthlySalaryReportListAPIView, MonthlySalaryGraphAPIView, NextSalaryPeriodAPIView, EmployeeSalaryRangeAPIView

urlpatterns = [
        # path('salary-sheet/', EmployeeSalarySheetAPIView.as_view(), name='employee-salary-sheet'),
        path("salary-sheet/employee/", EmployeeSalarySheetAPIView.as_view()),

        path('salary-sheet/branch/', BranchSalarySheetAPIView.as_view(), name='branch-salary-sheet'),
        path('salary-sheet/yearly/', EmployeeYearlySalarySheetAPIView.as_view(), name='employee-yearly-salary-sheet'),
        path('salary-sheet/branch/save/', SaveMonthlySalaryReportAPIView.as_view(), name='employee-yearly-salary-sheet-save'),

        path("branch/<int:branch_id>/salary-report/", MonthlySalaryReportDetailAPIView.as_view()),
        path("branch/<int:branch_id>/salary-report/history/", MonthlySalaryReportListAPIView.as_view()),
        path("branch/<int:branch_id>/salary-report/graph/", MonthlySalaryGraphAPIView.as_view()),                
        path("next-salary-period/", NextSalaryPeriodAPIView.as_view(), name="next-salary-period"),     

        path("branch/salary-report/employees/", EmployeeSalaryRangeAPIView.as_view(), name="employee-salary-range"),     
           
]