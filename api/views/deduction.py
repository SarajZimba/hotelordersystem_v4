from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models import tblDeduction
from api.serializers.deduction import tblDeductionSerializer

from django.db.models import Q

class DeductionCreateView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = tblDeductionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Deduction saved successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# views file

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from organization.models import Branch
from employee.models import MasterDeduction
from api.serializers.deduction import MasterDeductionSerializer


# known statutory deduction types — auto-fills based_on / waives_sst so admins
# don't need to understand the tax mechanics to configure these correctly.
# Anything not in this dict falls back to the model defaults (running_total / False),
# which the admin can still override explicitly via the payload.
# KNOWN_DEDUCTION_DEFAULTS = {
#     "social security fund": {"based_on": "basic_salary", "waives_sst": True},
#     "employees provident fund": {"based_on": "running_total", "waives_sst": False},
# }

# KNOWN_DEDUCTION_RATES = {
#     "ssf": {"calculation_type": "percentage", "default_value": Decimal("11.00")},
#     "social security fund": {"calculation_type": "percentage", "default_value": Decimal("11.00")},
#     "epf": {"calculation_type": "percentage", "default_value": Decimal("10.00")},
#     "employee provident fund": {"calculation_type": "percentage", "default_value": Decimal("10.00")},
# }

# def apply_known_deduction_defaults(data):
#     """
#     Mutates `data` in place, filling based_on/waives_sst from KNOWN_DEDUCTION_DEFAULTS
#     when the name matches a known type AND the admin didn't explicitly send a value.
#     """
#     name = (data.get("name") or "").strip().lower()
#     defaults = KNOWN_DEDUCTION_DEFAULTS.get(name)
#     if defaults:
#         if "based_on" not in data or data.get("based_on") in (None, ""):
#             data["based_on"] = defaults["based_on"]
#         if "waives_sst" not in data or data.get("waives_sst") is None:
#             data["waives_sst"] = defaults["waives_sst"]
#     return data

# from decimal import Decimal

# KNOWN_DEDUCTION_DEFAULTS = {
#     "social security fund": {
#         "based_on": "...",          # keep whatever you already have here
#         "waives_sst": True,          # keep whatever you already have here
#         "calculation_type": "percentage",
#         "default_value": Decimal("11.00"),
#     },
#     "ssf": {
#         "based_on": "...",
#         "waives_sst": True,
#         "calculation_type": "percentage",
#         "default_value": Decimal("11.00"),
#     },
#     "employee provident fund": {
#         "based_on": "...",
#         "waives_sst": False,
#         "calculation_type": "percentage",
#         "default_value": Decimal("10.00"),
#     },
#     "epf": {
#         "based_on": "...",
#         "waives_sst": False,
#         "calculation_type": "percentage",
#         "default_value": Decimal("10.00"),
#     },
# }

# def apply_known_deduction_defaults(data):
#     """
#     Mutates `data` in place.
#     - based_on / waives_sst: filled only if the admin didn't explicitly send them.
#     - calculation_type / default_value for known statutory types (SSF, EPF): always
#       forced to the statutory rate, since these are fixed by law and not admin-configurable.
#     """
#     name = (data.get("name") or "").strip().lower()
#     defaults = KNOWN_DEDUCTION_DEFAULTS.get(name)
#     if defaults:
#         if "based_on" not in data or data.get("based_on") in (None, ""):
#             data["based_on"] = defaults["based_on"]
#         if "waives_sst" not in data or data.get("waives_sst") is None:
#             data["waives_sst"] = defaults["waives_sst"]

#         # Statutory rate — always enforced, regardless of what the admin sent
#         data["calculation_type"] = defaults["calculation_type"]
#         data["default_value"] = defaults["default_value"]

#     return data


from decimal import Decimal

_SSF = {
    "based_on": "basic_salary",
    "waives_sst": True,
    "calculation_type": "percentage",
    "default_value": Decimal("11.00"),
}
_EPF = {
    "based_on": "basic_salary",
    "waives_sst": False,
    "calculation_type": "percentage",
    "default_value": Decimal("10.00"),
}

KNOWN_DEDUCTION_DEFAULTS = {
    "social security fund": _SSF,
    "ssf": _SSF,
    "employee provident fund": _EPF,
    "epf": _EPF,
}

def apply_known_deduction_defaults(data):
    """
    Mutates `data` in place.
    - based_on / waives_sst: filled only if the admin didn't explicitly send them.
    - calculation_type / default_value for known statutory types (SSF, EPF): always
      forced to the statutory rate, since these are fixed by law and not admin-configurable.
    """
    name = (data.get("name") or "").strip().lower()
    defaults = KNOWN_DEDUCTION_DEFAULTS.get(name)
    if defaults:
        if "based_on" not in data or data.get("based_on") in (None, ""):
            data["based_on"] = defaults["based_on"]
        if "waives_sst" not in data or data.get("waives_sst") is None:
            data["waives_sst"] = defaults["waives_sst"]

        # Statutory rate — always enforced, regardless of what the admin sent
        data["calculation_type"] = defaults["calculation_type"]
        data["default_value"] = defaults["default_value"]

    return data

class MasterDeductionListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        branch_id = request.query_params.get("branch")

        deductions = MasterDeduction.objects.all().order_by("order")
        if branch_id:
            deductions = deductions.filter(Q(branch_id=branch_id) | Q(branch__isnull=True))

        serializer = MasterDeductionSerializer(deductions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)

        name = data.get("name")
        if not name:
            return Response({"error": "name is required."}, status=status.HTTP_400_BAD_REQUEST)

        if data.get("default_value") in (None, ""):
            return Response({"error": "default_value is required."}, status=status.HTTP_400_BAD_REQUEST)

        # auto-fill based_on / waives_sst for known statutory deduction types,
        # unless the admin already explicitly provided them
        data = apply_known_deduction_defaults(data)

        calculation_type = data.get("calculation_type")
        if calculation_type not in ("percentage", "flat"):
            return Response(
                {"error": "calculation_type must be 'percentage' or 'flat'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        branch_id = data.get("branch")
        if branch_id:
            try:
                Branch.objects.get(id=branch_id)
            except (Branch.DoesNotExist, ValueError, TypeError):
                return Response({"error": "Invalid branch id."}, status=status.HTTP_400_BAD_REQUEST)

        if MasterDeduction.objects.filter(name__iexact=name.strip(), branch=branch_id).exists():
            return Response(
                {"error": f"A deduction named '{name}' already exists for this branch."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MasterDeductionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MasterDeductionDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return MasterDeduction.objects.get(pk=pk)
        except MasterDeduction.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        deduction = self.get_object(pk)
        if not deduction:
            return Response({"error": "MasterDeduction not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = MasterDeductionSerializer(deduction)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        deduction = self.get_object(pk)
        if not deduction:
            return Response({"error": "MasterDeduction not found."}, status=status.HTTP_404_NOT_FOUND)

        data = request.data.copy() if hasattr(request.data, "copy") else dict(request.data)

        # only re-apply auto-defaults if the name is changing AND the admin
        # didn't explicitly send based_on/waives_sst in this update
        if "name" in data and data["name"] != deduction.name:
            data = apply_known_deduction_defaults(data)

        calculation_type = data.get("calculation_type", deduction.calculation_type)
        if calculation_type not in ("percentage", "flat"):
            return Response(
                {"error": "calculation_type must be 'percentage' or 'flat'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        name = data.get("name", deduction.name)
        branch_id = data.get("branch", deduction.branch_id)

        duplicate = MasterDeduction.objects.filter(
            name__iexact=name.strip(), branch=branch_id
        ).exclude(pk=deduction.pk)
        if duplicate.exists():
            return Response(
                {"error": f"A deduction named '{name}' already exists for this branch."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MasterDeductionSerializer(deduction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        deduction = self.get_object(pk)
        if not deduction:
            return Response({"error": "MasterDeduction not found."}, status=status.HTTP_404_NOT_FOUND)

        linked_count = EmployeeDeduction.objects.filter(deduction=deduction).count()
        deduction.delete()
        return Response(
            {
                "message": "MasterDeduction deleted successfully.",
                "employee_overrides_also_deleted": linked_count
            },
            status=status.HTTP_200_OK
        )


# class MasterDeductionListCreateAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         branch_id = request.query_params.get("branch")

#         deductions = MasterDeduction.objects.all().order_by("order")
#         if branch_id:
#             from django.db.models import Q
#             deductions = deductions.filter(Q(branch_id=branch_id) | Q(branch__isnull=True))

#         serializer = MasterDeductionSerializer(deductions, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         data = request.data

#         name = data.get("name")
#         if not name:
#             return Response({"error": "name is required."}, status=status.HTTP_400_BAD_REQUEST)

#         calculation_type = data.get("calculation_type")
#         if calculation_type not in ("percentage", "flat"):
#             return Response(
#                 {"error": "calculation_type must be 'percentage' or 'flat'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         if data.get("default_value") in (None, ""):
#             return Response({"error": "default_value is required."}, status=status.HTTP_400_BAD_REQUEST)

#         branch_id = data.get("branch")
#         if branch_id:
#             try:
#                 Branch.objects.get(id=branch_id)
#             except (Branch.DoesNotExist, ValueError, TypeError):
#                 return Response({"error": "Invalid branch id."}, status=status.HTTP_400_BAD_REQUEST)

#         # prevent duplicate deduction names within the same branch scope
#         if MasterDeduction.objects.filter(name__iexact=name.strip(), branch=branch_id).exists():
#             return Response(
#                 {"error": f"A deduction named '{name}' already exists for this branch."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = MasterDeductionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class MasterDeductionDetailAPIView(APIView):
#     def get_object(self, pk):
#         try:
#             return MasterDeduction.objects.get(pk=pk)
#         except MasterDeduction.DoesNotExist:
#             return None

#     def get(self, request, pk, *args, **kwargs):
#         deduction = self.get_object(pk)
#         if not deduction:
#             return Response({"error": "MasterDeduction not found."}, status=status.HTTP_404_NOT_FOUND)
#         serializer = MasterDeductionSerializer(deduction)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def put(self, request, pk, *args, **kwargs):
#         deduction = self.get_object(pk)
#         if not deduction:
#             return Response({"error": "MasterDeduction not found."}, status=status.HTTP_404_NOT_FOUND)

#         data = request.data
#         calculation_type = data.get("calculation_type", deduction.calculation_type)
#         if calculation_type not in ("percentage", "flat"):
#             return Response(
#                 {"error": "calculation_type must be 'percentage' or 'flat'."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         name = data.get("name", deduction.name)
#         branch_id = data.get("branch", deduction.branch_id)

#         # duplicate check, excluding this row itself
#         duplicate = MasterDeduction.objects.filter(
#             name__iexact=name.strip(), branch=branch_id
#         ).exclude(pk=deduction.pk)
#         if duplicate.exists():
#             return Response(
#                 {"error": f"A deduction named '{name}' already exists for this branch."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = MasterDeductionSerializer(deduction, data=data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, *args, **kwargs):
#         deduction = self.get_object(pk)
#         if not deduction:
#             return Response({"error": "MasterDeduction not found."}, status=status.HTTP_404_NOT_FOUND)

#         # warn if employees have overrides tied to this deduction — deleting cascades to them
#         from employee.models import EmployeeDeduction
#         linked_count = EmployeeDeduction.objects.filter(deduction=deduction).count()

#         deduction.delete()
#         return Response(
#             {
#                 "message": "MasterDeduction deleted successfully.",
#                 "employee_overrides_also_deleted": linked_count
#             },
#             status=status.HTTP_200_OK
#         )


from employee.models import Employee, EmployeeDeduction, MasterDeduction
from api.serializers.deduction import EmployeeDeductionSerializer


# class EmployeeDeductionListCreateAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         emp_id = request.query_params.get("empID")

#         assignments = EmployeeDeduction.objects.all()
#         if emp_id:
#             assignments = assignments.filter(empID_id=emp_id)

#         serializer = EmployeeDeductionSerializer(assignments, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         data = request.data

#         emp_id = data.get("empID")
#         if not emp_id:
#             return Response({"error": "empID is required."}, status=status.HTTP_400_BAD_REQUEST)

#         deduction_id = data.get("deduction")
#         if not deduction_id:
#             return Response({"error": "deduction is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             Employee.objects.get(id=emp_id)
#         except (Employee.DoesNotExist, ValueError, TypeError):
#             return Response({"error": "Invalid empID."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             MasterDeduction.objects.get(id=deduction_id)
#         except (MasterDeduction.DoesNotExist, ValueError, TypeError):
#             return Response({"error": "Invalid deduction id."}, status=status.HTTP_400_BAD_REQUEST)

#         # prevent duplicate assignment of the same deduction to the same employee
#         if EmployeeDeduction.objects.filter(empID_id=emp_id, deduction_id=deduction_id).exists():
#             return Response(
#                 {"error": "This deduction is already assigned to this employee. Use PUT to update its value."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = EmployeeDeductionSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from employee.models import Employee, EmployeeDeduction, MasterDeduction
from api.serializers.deduction import EmployeeDeductionSerializer
from django.shortcuts import get_object_or_404

class EmployeeDeductionListCreateAPIView(APIView):
    # def get(self, request, *args, **kwargs):
    #     emp_id = request.query_params.get("empID")

    #     assignments = EmployeeDeduction.objects.all()
    #     if emp_id:
    #         assignments = assignments.filter(empID_id=emp_id)

    #     serializer = EmployeeDeductionSerializer(assignments, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # def get(self, request, *args, **kwargs):
    #     emp_id = request.query_params.get("empID")

    #     assignments = EmployeeDeduction.objects.select_related("deduction", "empID").all()
    #     if emp_id:
    #         assignments = assignments.filter(empID_id=emp_id)

    #     data = []
    #     for assignment in assignments:
    #         data.append({
    #             "id": assignment.id,
    #             "empID": assignment.empID_id,
    #             "deduction": assignment.deduction_id,
    #             "deduction_name": assignment.deduction.name,
    #             "calculation_type": assignment.deduction.calculation_type,
    #             "default_value": assignment.deduction.default_value,
    #             "based_on": assignment.deduction.based_on,
    #             "waives_sst": assignment.deduction.waives_sst,
    #             "value": assignment.value,
    #         })

    #     return Response(data, status=status.HTTP_200_OK)


    def get(self, request, *args, **kwargs):
        emp_id = request.query_params.get("empID")

        # One employee: everything the salary sheet deducts for them
        if emp_id:
            employee = get_object_or_404(Employee, pk=emp_id)

            masters = MasterDeduction.objects.filter(used=True).filter(
                Q(branch_id=employee.branch_id) | Q(branch__isnull=True)
            ).order_by("order")

            overrides = {
                ed.deduction_id: ed
                for ed in EmployeeDeduction.objects.filter(empID=employee)
            }

            data = []
            for master in masters:
                override = overrides.get(master.id)
                value = (
                    override.value
                    if override is not None and override.value is not None
                    else master.default_value
                )
                data.append({
                    "id": override.id if override else None,  # None = comes from the master deduction
                    "empID": employee.id,
                    "deduction": master.id,
                    "deduction_name": master.name,
                    "calculation_type": master.calculation_type,
                    "default_value": master.default_value,
                    "based_on": master.based_on,
                    "waives_sst": master.waives_sst,
                    "value": value,  # the value the salary sheet uses
                    "source": "assigned" if override else "default",
                })
            return Response(data, status=status.HTTP_200_OK)

        # No employee: the original list of assignment rows
        assignments = EmployeeDeduction.objects.select_related("deduction", "empID").all()
        data = [
            {
                "id": a.id,
                "empID": a.empID_id,
                "deduction": a.deduction_id,
                "deduction_name": a.deduction.name,
                "calculation_type": a.deduction.calculation_type,
                "default_value": a.deduction.default_value,
                "based_on": a.deduction.based_on,
                "waives_sst": a.deduction.waives_sst,
                "value": a.value,
            }
            for a in assignments
        ]
        return Response(data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        payload = request.data

        # Normalize: accept either a single object or a list of objects
        is_bulk = isinstance(payload, list)
        items = payload if is_bulk else [payload]

        if not items:
            return Response({"error": "No deduction data provided."}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        errors = []

        for index, data in enumerate(items):
            if not isinstance(data, dict):
                errors.append({"index": index, "error": "Each item must be an object."})
                continue

            emp_id = data.get("empID")
            if not emp_id:
                errors.append({"index": index, "error": "empID is required."})
                continue

            deduction_id = data.get("deduction")
            if not deduction_id:
                errors.append({"index": index, "error": "deduction is required."})
                continue

            try:
                Employee.objects.get(id=emp_id)
            except (Employee.DoesNotExist, ValueError, TypeError):
                errors.append({"index": index, "empID": emp_id, "error": "Invalid empID."})
                continue

            try:
                MasterDeduction.objects.get(id=deduction_id)
            except (MasterDeduction.DoesNotExist, ValueError, TypeError):
                errors.append({"index": index, "empID": emp_id, "error": "Invalid deduction id."})
                continue

            # prevent duplicate assignment of the same deduction to the same employee
            if EmployeeDeduction.objects.filter(empID_id=emp_id, deduction_id=deduction_id).exists():
                errors.append({
                    "index": index,
                    "empID": emp_id,
                    "deduction": deduction_id,
                    "error": "This deduction is already assigned to this employee. Use PUT to update its value."
                })
                continue

            serializer = EmployeeDeductionSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                results.append(serializer.data)
            else:
                errors.append({"index": index, "empID": emp_id, "error": serializer.errors})

        if not is_bulk:
            # Preserve original single-object behavior exactly
            if errors:
                return Response(errors[0].get("error", errors[0]), status=status.HTTP_400_BAD_REQUEST)
            return Response(results[0], status=status.HTTP_201_CREATED)

        # Bulk response: report both successes and failures, don't let one bad row block the rest
        response_status = status.HTTP_201_CREATED if results and not errors else (
            status.HTTP_207_MULTI_STATUS if results and errors else status.HTTP_400_BAD_REQUEST
        )
        return Response(
            {"created": results, "errors": errors, "created_count": len(results), "error_count": len(errors)},
            status=response_status
        )


class EmployeeDeductionDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return EmployeeDeduction.objects.get(pk=pk)
        except EmployeeDeduction.DoesNotExist:
            return None

    def get(self, request, pk, *args, **kwargs):
        assignment = self.get_object(pk)
        if not assignment:
            return Response({"error": "EmployeeDeduction not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = EmployeeDeductionSerializer(assignment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        assignment = self.get_object(pk)
        if not assignment:
            return Response({"error": "EmployeeDeduction not found."}, status=status.HTTP_404_NOT_FOUND)

        # only value should typically change here — empID/deduction stay fixed
        serializer = EmployeeDeductionSerializer(assignment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        assignment = self.get_object(pk)
        if not assignment:
            return Response({"error": "EmployeeDeduction not found."}, status=status.HTTP_404_NOT_FOUND)

        assignment.delete()
        return Response({"message": "EmployeeDeduction override removed."}, status=status.HTTP_200_OK)