from django.db import models

# Create your models here.
from django.db import models
from django.db.models import UniqueConstraint

from root.utils import BaseModel
from employee.models import Employee
from organization.models import Branch


class MonthlySalaryReport(BaseModel):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="salary_reports")
    month = models.CharField(max_length=50, null=True)
    nepali_year = models.CharField(max_length=50, null=True)
    nepali_date = models.CharField(max_length=50, null=True)
    fiscal_year = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=["branch", "nepali_year", "month"], name="unique_branch_month_report")
        ]

    def __str__(self):
        return f"{self.branch} — {self.month} {self.nepali_year}"


class EmployeeSalary(BaseModel):
    monthly_report = models.ForeignKey(MonthlySalaryReport, on_delete=models.CASCADE, related_name="employee_salaries")
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)

    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)   # pre-deduction
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)   # post leave+fund deduction
    net_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # no scalar tax_deduction field anymore — it's a breakdown, see TaxDeduction below

    class Meta:
        constraints = [
            UniqueConstraint(fields=["monthly_report", "empID"], name="unique_employee_per_report")
        ]

    def __str__(self):
        return self.name or str(self.empID_id)


class EmployeeSalaryPayPackage(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name="pay_packages", on_delete=models.CASCADE)
    package_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    package_type = models.CharField(max_length=50, null=True, blank=True)
    taxable = models.BooleanField(null=True, default=None)  # source can return null (e.g. "Allowance")

    def __str__(self):
        return self.package_name


class LeaveDeduction(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name="leave_deductions", on_delete=models.CASCADE)
    unpaid_leavesdeduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unpaid_leaves = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Leave Deduction for {self.employee.name}"


class FundDeduction(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name="fund_deductions", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name


class TaxDeduction(BaseModel):
    employee = models.ForeignKey(EmployeeSalary, related_name="tax_deductions", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)      # "SST", "Income Tax", "Total Tax"
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name