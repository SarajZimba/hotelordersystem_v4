from rest_framework import serializers
from employee.models import Employee

from employee.models import Pay_Package, MasterPayPackage

class PayPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pay_Package
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         exclude = [
#             # "created_at",
#             "updated_at",
#             "status",
#             "is_deleted",
#             "sorting_order",
#             "is_featured"
#         ]

# from django.contrib.auth.hashers import make_password

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         exclude = [
#             # "created_at",
#             "updated_at",
#             "status",
#             "is_deleted",
#             "sorting_order",
#             "is_featured",
#         ]
#         extra_kwargs = {
#             "password": {"write_only": True},
#         }

#     def validate_username(self, value):
#         return value or None

#     def validate(self, attrs):
#         if self.instance is None:  # create only
#             errors = {}
#             if not attrs.get("username"):
#                 errors["username"] = "This field is required."
#             if not attrs.get("password"):
#                 errors["password"] = "This field is required."
#             if errors:
#                 raise serializers.ValidationError(errors)
#         return attrs

#     def create(self, validated_data):
#         if validated_data.get("password"):
#             validated_data["password"] = make_password(validated_data["password"])
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         pwd = validated_data.pop("password", None)
#         if pwd:
#             validated_data["password"] = make_password(pwd)
#         return super().update(instance, validated_data)


from django.contrib.auth.hashers import make_password


# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         exclude = [
#             # "created_at",
#             "updated_at",
#             "status",
#             "is_deleted",
#             "sorting_order",
#             "is_featured",
#         ]
#         extra_kwargs = {
#             "password": {"write_only": True},
#         }

#     def validate_username(self, value):
#         return value or None

#     def validate(self, attrs):
#         errors = {}
#         if self.instance is None:  # create
#             if not attrs.get("username"):
#                 errors["username"] = "This field is required."
#             if not attrs.get("password"):
#                 errors["password"] = "This field is required."
#         else:  # update: username can be left out, but not blanked
#             if "username" in attrs and not attrs["username"]:
#                 errors["username"] = "This field may not be blank."
#         if errors:
#             raise serializers.ValidationError(errors)
#         return attrs

#     def create(self, validated_data):
#         if validated_data.get("password"):
#             validated_data["password"] = make_password(validated_data["password"])
#         return super().create(validated_data)

#     def update(self, instance, validated_data):
#         pwd = validated_data.pop("password", None)
#         if pwd:
#             validated_data["password"] = make_password(pwd)
#         return super().update(instance, validated_data)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured",
        ]
        # No write_only: the password is returned in responses so HR can see it.
        # Add extra_kwargs = {"password": {"write_only": True}} to hide it again.

    def validate_username(self, value):
        return value or None

    def validate(self, attrs):
        errors = {}
        if self.instance is None:  # create
            if not attrs.get("username"):
                errors["username"] = "This field is required."
            if not attrs.get("password"):
                errors["password"] = "This field is required."
        else:  # update: username can be left out, but not blanked
            if "username" in attrs and not attrs["username"]:
                errors["username"] = "This field may not be blank."
        if errors:
            raise serializers.ValidationError(errors)
        return attrs
        
class EmployeePayPackageSerializer(serializers.ModelSerializer):
    pay_packages = PayPackageSerializer(many=True, read_only=True, source='pay_package_set')
    class Meta:
        model = Employee
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

from employee.models import DailyAttendance

class DailyAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyAttendance
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]
        
class MasterPayPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterPayPackage
        exclude = [
            # "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

from employee.models import tblEmployeeCIT

class tblEmployeeCITSerializer(serializers.ModelSerializer):
    employee_name = serializers.SerializerMethodField()
    class Meta:
        model = tblEmployeeCIT
        exclude = [
            "created_at",
            "updated_at",
            "status",
            "is_deleted",
            "sorting_order",
            "is_featured"
        ]

    def get_employee_name(self, obj):
        return obj.empID.name