from rest_framework import serializers
from employee.models import tblDeduction

class tblDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = tblDeduction
        fields = ['id', 'name', 'used']


# api/serializers/employee.py

from rest_framework import serializers
from employee.models import MasterDeduction, EmployeeDeduction


class MasterDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterDeduction
        fields = [
            "id", "name", "calculation_type", "default_value",
            "based_on", "waives_sst", "order", "used", "branch"
        ]


class EmployeeDeductionSerializer(serializers.ModelSerializer):
    deduction_name = serializers.CharField(source="deduction.name", read_only=True)
    employee_name = serializers.CharField(source="empID.name", read_only=True)

    class Meta:
        model = EmployeeDeduction
        fields = [
            "id", "empID", "employee_name", "deduction", "deduction_name", "value"
        ]