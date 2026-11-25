from django.db import models
from root.utils import BaseModel
# Create your models here.
from organization.models import Branch
from django.contrib.auth.hashers import make_password, check_password

class Employee(BaseModel):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True)
    hiring_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=100, null=True)
    marital_status = models.CharField(max_length=100,null=True)
    current_status = models.CharField(max_length=100, null=True) 
    branch = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE) 
    level = models.CharField(max_length=100, null=True) 
    termination_date = models.DateField(null=True)
    shift = models.CharField(null=True, max_length=50)
    attendance_required = models.BooleanField(null=True)
    lateattendance_alert = models.BooleanField(null=True)
    pic = models.ImageField(
        upload_to="employee/images/", null=True, blank=True
    )
    department = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return bool(self.password) and check_password(raw_password, self.password)

class DailyAttendance(BaseModel):
    attendance_date = models.DateField()
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    check_in = models.TimeField(null=True)
    check_out = models.TimeField(null=True)
    total_time = models.TimeField(null=True)
    is_completed = models.BooleanField(default=True)
    late_attendance_flag = models.BooleanField(null=True)
    no_show_flag = models.BooleanField(null=True)

class MasterPayPackage(BaseModel):
    package_name = models.CharField(max_length=100)
    package_type = models.CharField(max_length=100, null=True)
    taxable = models.BooleanField(null=True)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE) 


class Pay_Package(BaseModel):
    # package_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # package_type = models.CharField(max_length=100, null=True)
    # taxable = models.BooleanField(null=True)
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    package = models.ForeignKey(MasterPayPackage, on_delete=models.CASCADE, null=True)

class tblpaidleaves(BaseModel):
    empID = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True)
    no_of_leaves = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class tblcompanypaidleavePolicy(BaseModel):
    noOfdays = models.DecimalField(max_digits=10, decimal_places=2, default=2.5)


class tblleaveapply(BaseModel):
    empID = models.ForeignKey(Employee, models.CASCADE)
    applyDate = models.DateField(null=True)
    noOfDays = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    noOfPaidLeaves = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    noOfUnPaidLeaves = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leaveDateFrom = models.DateField(null=True)
    leaveDateTo = models.DateField(null=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    current_status = models.CharField(max_length=200, null=True, blank=True)   
    leaveDateFrom_np = models.CharField(max_length=200, null=True, blank=True)
    leaveDateTo_np = models.CharField(max_length=200, null=True, blank=True)
    nepali_month = models.CharField(max_length=200, null=True, blank=True)
    nepali_year = models.CharField(max_length=200, null=True, blank=True)
    noOfPaidLeaves_taken = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    
class tblEmployeeSalary(BaseModel):
    emp_ID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    taxable = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    non_taxable = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
class tblDeduction(BaseModel):

    name = models.CharField(max_length=50, null=True)
    used = models.BooleanField(default=False)
    
    
class tblEmployeeCommision(BaseModel):
    empID = models.ForeignKey(Employee, models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    month = models.CharField(max_length=200, null=True)
    type = models.CharField(max_length=100, null=True)

class tblEmployeeCIT(BaseModel):
    empID = models.ForeignKey(Employee, models.CASCADE, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
from django.db import models

# Create your models here.


class MasterDeduction(BaseModel):
    CALCULATION_CHOICES = [
        ("percentage", "Percentage"),
        ("flat", "Flat Amount"),
    ]
    BASE_CHOICES = [
        ("basic_salary", "Basic Salary"),
        ("running_total", "Running Total (after prior deductions)"),
        ("gross_salary", "Gross Salary (before any deductions)"),
    ]

    name = models.CharField(max_length=100)
    calculation_type = models.CharField(max_length=20, choices=CALCULATION_CHOICES)
    default_value = models.DecimalField(max_digits=10, decimal_places=2)
    based_on = models.CharField(max_length=20, choices=BASE_CHOICES, default="running_total")
    waives_sst = models.BooleanField(default=False)  # True only for SSF — marks that SST tax should be skipped
    order = models.PositiveIntegerField(default=0)
    used = models.BooleanField(default=True)
    branch = models.ForeignKey(Branch, null=True, on_delete=models.CASCADE)


class EmployeeDeduction(BaseModel):
    empID = models.ForeignKey(Employee, on_delete=models.CASCADE)
    deduction = models.ForeignKey(MasterDeduction, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)