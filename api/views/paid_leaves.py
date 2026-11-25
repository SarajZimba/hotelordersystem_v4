from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.paid_leaves import tblcompanypaidleavePolicySerializer
from employee.models import tblcompanypaidleavePolicy, tblleaveapply
from datetime import datetime

class tblcompanypaidleavePolicyCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            policy = tblcompanypaidleavePolicy.objects.first()  # Get the first (and only) policy
            if not policy:
                return Response({"detail": "No policy found."}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = tblcompanypaidleavePolicySerializer(policy)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            policy = tblcompanypaidleavePolicy.objects.first()  # Check for an existing policy
            if policy:
                # Update the existing policy
                serializer = tblcompanypaidleavePolicySerializer(policy, data=request.data, partial=True)
            else:
                # Create a new policy if none exists
                serializer = tblcompanypaidleavePolicySerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK if policy else status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# from employee.models import Employee

# from employee.models import tblpaidleaves
# class tblleaveapplyCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         # Get empID from the request
#         empID = data.get("empID")
#         if empID is None:
#             return Response({"error": "No employee selected"}, status=400)

#         # Fetch employee instance
#         try:
#             employee = Employee.objects.get(id=int(empID))
#         except Employee.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=404)


#         # Get leave dates and reason
#         leave_date_from = data.get("leave_date_from")
#         leave_date_to = data.get("leave_date_to")
#         reason = data.get("reason", None)

#         if not leave_date_from or not leave_date_to:
#             return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)

#         # Convert leave dates to date objects
#         try:
#             leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
#             leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#         # Calculate noOfDays (inclusive difference)
#         no_of_days = (leave_date_to - leave_date_from).days + 1
#         if no_of_days <= 0:
#             return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

#         # Fetch the no of paid leaves 
#         employees_paid_leaves_data = tblpaidleaves.objects.get(empID= employee)

#         if employees_paid_leaves_data.no_of_leaves < no_of_days:
#             holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
#             employees_paid_leaves_data.no_of_leaves = 0
#             employees_paid_leaves_data.save()
#             difference_for_unpaid_leaves_for_tblleaveapply = no_of_days - holder_for_employees_previous_paid_leaves
#             difference_for_paid_leaves_for_tblleaveapply = holder_for_employees_previous_paid_leaves

#         else:
#             holder_for_employees_previous_paid_leaves = employees_paid_leaves_data.no_of_leaves
#             difference_for_paid_leaves_for_tblleaveapply = holder_for_employees_previous_paid_leaves - no_of_days
#             difference_for_unpaid_leaves_for_tblleaveapply = 0
#             employees_paid_leaves_data.no_of_leaves = difference_for_paid_leaves_for_tblleaveapply
#             employees_paid_leaves_data.save()



#         # Set applyDate to today's date
#         apply_date = datetime.today().date()

#         # Create tblleaveapply object
#         leave_apply = tblleaveapply.objects.create(
#             empID=employee,
#             applyDate=apply_date,
#             noOfDays=no_of_days,
#             leaveDateFrom=leave_date_from,
#             leaveDateTo=leave_date_to,
#             reason=reason,
#             noOfPaidLeaves = difference_for_paid_leaves_for_tblleaveapply,
#             noOfUnPaidLeaves = difference_for_unpaid_leaves_for_tblleaveapply

#         )

#         # Serialize and return the created object (if needed)
#         response_data = {
#             "id": leave_apply.id,
#             "empID": leave_apply.empID.id,
#             "applyDate": leave_apply.applyDate,
#             "noOfDays": leave_apply.noOfDays,
#             "leaveDateFrom": leave_apply.leaveDateFrom,
#             "leaveDateTo": leave_apply.leaveDateTo,
#             "reason": leave_apply.reason,
#             "noOfPaidLeaves": leave_apply.noOfPaidLeaves,
#             "noofUnPaidLeaves": leave_apply.noOfUnPaidLeaves,
#         }

#         return Response(response_data, status=status.HTTP_201_CREATED)  

from employee.models import Employee
import nepali_datetime
from datetime import timedelta

from employee.utils import convert_eng_to_nepali
from employee.models import tblpaidleaves
import json

# from django.db import transaction
# class tblleaveapplyCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         empID = data.get("empID")
#         if empID is None:
#             return Response({"error": "No employee selected"}, status=400)

#         try:
#             employee = Employee.objects.get(id=int(empID))
#         except Employee.DoesNotExist:
#             return Response({"error": "Employee not found"}, status=404)

#         leave_date_from = data.get("leave_date_from")
#         leave_date_to = data.get("leave_date_to")
#         reason = data.get("reason", None)

#         if not leave_date_from or not leave_date_to:
#             return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)

#         nepali_year, converted_nepali_date = convert_eng_to_nepali(leave_date_from)

#         try:
#             leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
#             leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#         no_of_days = (leave_date_to - leave_date_from).days + 1
#         if no_of_days <= 0:
#             return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

#         # Nepali month breakdown — doesn't touch the DB, safe to compute outside the transaction
#         nepali_month_count = {}
#         current_date = leave_date_from
#         while current_date <= leave_date_to:
#             nepali_date = nepali_datetime.date.from_datetime_date(current_date)
#             nepali_month = nepali_date.strftime("%B")
#             nepali_month_count[nepali_month] = nepali_month_count.get(nepali_month, 0) + 1
#             current_date += timedelta(days=1)
#         nepali_month_json = json.dumps(nepali_month_count)

#         apply_date = datetime.today().date()

#         try:
#             with transaction.atomic():
#                 employees_paid_leaves_data = tblpaidleaves.objects.select_for_update().get(empID=employee)

#                 if employees_paid_leaves_data.no_of_leaves < no_of_days:
#                     holder = employees_paid_leaves_data.no_of_leaves
#                     employees_paid_leaves_data.no_of_leaves = 0
#                     difference_for_unpaid_leaves = no_of_days - holder
#                     difference_for_paid_leaves = 0.0
#                     no_of_paidleaves_taken = holder
#                 else:
#                     holder = employees_paid_leaves_data.no_of_leaves
#                     difference_for_paid_leaves = holder - no_of_days
#                     difference_for_unpaid_leaves = 0
#                     employees_paid_leaves_data.no_of_leaves = difference_for_paid_leaves
#                     no_of_paidleaves_taken = no_of_days

#                 employees_paid_leaves_data.save()

#                 leave_apply = tblleaveapply.objects.create(
#                     empID=employee,
#                     applyDate=apply_date,
#                     noOfDays=no_of_days,
#                     leaveDateFrom=leave_date_from,
#                     leaveDateTo=leave_date_to,
#                     reason=reason,
#                     noOfPaidLeaves=difference_for_paid_leaves,
#                     noOfUnPaidLeaves=difference_for_unpaid_leaves,
#                     nepali_month=nepali_month_json,
#                     nepali_year=nepali_year,
#                     leaveDateFrom_np=converted_nepali_date,
#                     noOfPaidLeaves_taken=no_of_paidleaves_taken,
#                     current_status="Approved",
#                 )
#         except tblpaidleaves.DoesNotExist:
#             return Response({"error": "Paid leave record not found for this employee."}, status=404)

#         response_data = {
#             "id": leave_apply.id,
#             "empID": leave_apply.empID.id,
#             "applyDate": leave_apply.applyDate,
#             "noOfDays": leave_apply.noOfDays,
#             "leaveDateFrom": leave_apply.leaveDateFrom,
#             "leaveDateTo": leave_apply.leaveDateTo,
#             "reason": leave_apply.reason,
#             "noOfPaidLeaves": leave_apply.noOfPaidLeaves,
#             "noOfUnPaidLeaves": leave_apply.noOfUnPaidLeaves,
#             "current_status": leave_apply.current_status,
#         }
#         return Response(response_data, status=status.HTTP_201_CREATED)

ALLOWED_LEAVE_STATUSES = {"Pending", "Approved", "Cancelled"}

from datetime import timedelta
from decimal import Decimal

import nepali_datetime

# Build month names from the library so spellings always match what strftime("%B") gives you
NEPALI_MONTHS = [nepali_datetime.date(2080, m, 1).strftime("%B") for m in range(1, 13)]
MONTH_INDEX = {name.lower(): i for i, name in enumerate(NEPALI_MONTHS)}

def nepali_month_range(nepali_year, nepali_month):
    """First and last English dates of a Nepali month."""
    m = NEPALI_MONTHS.index(nepali_month) + 1
    year = int(nepali_year)
    start = nepali_datetime.date(year, m, 1).to_datetime_date()
    if m == 12:
        next_start = nepali_datetime.date(year + 1, 1, 1).to_datetime_date()
    else:
        next_start = nepali_datetime.date(year, m + 1, 1).to_datetime_date()
    return start, next_start - timedelta(days=1)


def approved_leave_days_in_month(employee, nepali_year, nepali_month):
    start, end = nepali_month_range(nepali_year, nepali_month)
    leaves = tblleaveapply.objects.filter(
        empID=employee,
        current_status="Approved",
        leaveDateFrom__lte=end,
        leaveDateTo__gte=start,
    )
    total = Decimal("0")
    for leave in leaves:
        first = max(leave.leaveDateFrom, start)
        last = min(leave.leaveDateTo, end)
        total += Decimal((last - first).days + 1)
    return total


def get_leave_summary(employee, nepali_year, nepali_month):
    allowance = employee.branch.noOfpaidleavesallowed if employee.branch else Decimal("0")
    used = approved_leave_days_in_month(employee, nepali_year, nepali_month)
    paid = min(used, allowance)
    return {
        "allowance": allowance,
        "used_days": used,
        "paid_days": paid,
        "unpaid_days": used - paid,
        "remaining": allowance - paid,
    }
from django.db import transaction


class tblleaveapplyCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        empID = data.get("empID")
        if empID is None:
            return Response({"error": "No employee selected"}, status=400)

        try:
            employee = Employee.objects.get(id=int(empID))
        except (Employee.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Employee not found"}, status=404)

        leave_date_from = data.get("leave_date_from")
        leave_date_to = data.get("leave_date_to")
        reason = data.get("reason", None)

        if not leave_date_from or not leave_date_to:
            return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)

        # Validate dates BEFORE converting them
        try:
            leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
            leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        no_of_days = (leave_date_to - leave_date_from).days + 1
        if no_of_days <= 0:
            return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

        nepali_year, converted_nepali_date = convert_eng_to_nepali(leave_date_from.strftime("%Y-%m-%d"))
        _, converted_nepali_date_to = convert_eng_to_nepali(leave_date_to.strftime("%Y-%m-%d"))

        # Nepali month breakdown, plus the (year, month) pairs the leave touches
        nepali_month_count = {}
        months_touched = []
        current_date = leave_date_from
        while current_date <= leave_date_to:
            nepali_date = nepali_datetime.date.from_datetime_date(current_date)
            nepali_month = nepali_date.strftime("%B")
            nepali_month_count[nepali_month] = nepali_month_count.get(nepali_month, 0) + 1
            if (nepali_date.year, nepali_month) not in months_touched:
                months_touched.append((nepali_date.year, nepali_month))
            current_date += timedelta(days=1)
        nepali_month_json = json.dumps(nepali_month_count)

        apply_date = datetime.today().date()

        with transaction.atomic():
            # Lock the employee row so two simultaneous applications can't both pass the overlap check
            Employee.objects.select_for_update().get(pk=employee.pk)

            # Block overlapping applications (Cancelled ones don't count)
            overlap = tblleaveapply.objects.filter(
                empID=employee,
                leaveDateFrom__lte=leave_date_to,
                leaveDateTo__gte=leave_date_from,
            ).exclude(current_status="Cancelled").exists()
            if overlap:
                return Response(
                    {"error": "Leave already applied for some of these dates."},
                    status=400,
                )

            leave_apply = tblleaveapply.objects.create(
                empID=employee,
                applyDate=apply_date,
                noOfDays=no_of_days,
                leaveDateFrom=leave_date_from,
                leaveDateTo=leave_date_to,
                reason=reason,
                nepali_month=nepali_month_json,
                nepali_year=nepali_year,
                leaveDateFrom_np=converted_nepali_date,
                leaveDateTo_np=converted_nepali_date_to,
                current_status="Approved",
            )

        month_summaries = [
            {"year": year, "month": month, **get_leave_summary(employee, year, month)}
            for year, month in months_touched
        ]

        response_data = {
            "id": leave_apply.id,
            "empID": leave_apply.empID.id,
            "applyDate": leave_apply.applyDate,
            "noOfDays": leave_apply.noOfDays,
            "leaveDateFrom": leave_apply.leaveDateFrom,
            "leaveDateTo": leave_apply.leaveDateTo,
            "reason": leave_apply.reason,
            "current_status": leave_apply.current_status,
            "month_summaries": month_summaries,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)



# class tblleaveapplyUpdateAPIView(APIView):
#     def patch(self, request, pk, *args, **kwargs):
#         data = request.data

#         try:
#             with transaction.atomic():
#                 leave = tblleaveapply.objects.select_for_update().get(pk=pk)
#                 employee = leave.empID

#                 if leave.current_status == "Cancelled":
#                     return Response({"error": "Cancelled leave cannot be edited."}, status=400)

#                 new_date_from_str = data.get("leave_date_from")
#                 new_date_to_str = data.get("leave_date_to")
#                 leave.reason = data.get("reason", leave.reason)

#                 if new_date_from_str or new_date_to_str:
#                     try:
#                         leave_date_from = (
#                             datetime.strptime(new_date_from_str, "%Y-%m-%d").date()
#                             if new_date_from_str else leave.leaveDateFrom
#                         )
#                         leave_date_to = (
#                             datetime.strptime(new_date_to_str, "%Y-%m-%d").date()
#                             if new_date_to_str else leave.leaveDateTo
#                         )
#                     except ValueError:
#                         return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#                     no_of_days = (leave_date_to - leave_date_from).days + 1
#                     if no_of_days <= 0:
#                         return Response(
#                             {"error": "leave_date_to must be greater than or equal to leave_date_from."},
#                             status=400,
#                         )

#                     overlap = tblleaveapply.objects.filter(
#                         empID=employee,
#                         leaveDateFrom__lte=leave_date_to,
#                         leaveDateTo__gte=leave_date_from,
#                     ).exclude(pk=leave.pk).exclude(current_status="Cancelled").exists()
#                     if overlap:
#                         return Response({"error": "Leave already applied for some of these dates but is in Cancelled State"}, status=400)

#                     paid_record = tblpaidleaves.objects.select_for_update().get(empID=employee)
#                     is_approved = leave.current_status == "Approved"

#                     # Only an Approved leave has actually deducted from the balance
#                     available = paid_record.no_of_leaves
#                     if is_approved:
#                         available += leave.noOfPaidLeaves_taken

#                     days = Decimal(no_of_days)
#                     if available < days:
#                         paid_taken = available
#                         unpaid_days = days - available
#                         balance_after = Decimal("0")
#                     else:
#                         paid_taken = days
#                         unpaid_days = Decimal("0")
#                         balance_after = available - days

#                     if is_approved:
#                         paid_record.no_of_leaves = balance_after
#                         paid_record.save()

#                     nepali_month_count = {}
#                     current_date = leave_date_from
#                     while current_date <= leave_date_to:
#                         nepali_month = nepali_datetime.date.from_datetime_date(current_date).strftime("%B")
#                         nepali_month_count[nepali_month] = nepali_month_count.get(nepali_month, 0) + 1
#                         current_date += timedelta(days=1)

#                     nepali_year, np_from = convert_eng_to_nepali(leave_date_from.strftime("%Y-%m-%d"))
#                     _, np_to = convert_eng_to_nepali(leave_date_to.strftime("%Y-%m-%d"))

#                     leave.leaveDateFrom = leave_date_from
#                     leave.leaveDateTo = leave_date_to
#                     leave.noOfDays = no_of_days
#                     leave.noOfPaidLeaves = balance_after
#                     leave.noOfUnPaidLeaves = unpaid_days
#                     leave.noOfPaidLeaves_taken = paid_taken
#                     leave.nepali_month = json.dumps(nepali_month_count)
#                     leave.nepali_year = nepali_year
#                     leave.leaveDateFrom_np = np_from
#                     leave.leaveDateTo_np = np_to

#                 leave.save()

#         except tblleaveapply.DoesNotExist:
#             return Response({"error": "Leave application not found."}, status=404)
#         except tblpaidleaves.DoesNotExist:
#             return Response({"error": "Paid leave record not found for this employee."}, status=404)

#         return Response(
#             {
#                 "message": "Leave application updated successfully.",
#                 "id": leave.id,
#                 "leaveDateFrom": leave.leaveDateFrom,
#                 "leaveDateTo": leave.leaveDateTo,
#                 "noOfDays": leave.noOfDays,
#                 "noOfPaidLeaves": leave.noOfPaidLeaves,
#                 "noOfUnPaidLeaves": leave.noOfUnPaidLeaves,
#                 "noOfPaidLeaves_taken": leave.noOfPaidLeaves_taken,
#                 "current_status": leave.current_status,
#                 "reason": leave.reason,
#             },
#             status=status.HTTP_200_OK,
#         )


class tblleaveapplyUpdateAPIView(APIView):
    def patch(self, request, pk, *args, **kwargs):
        data = request.data

        try:
            with transaction.atomic():
                leave = tblleaveapply.objects.select_for_update().get(pk=pk)
                employee = leave.empID

                # Serialize with other applications from the same employee (overlap check)
                Employee.objects.select_for_update().get(pk=employee.pk)

                if leave.current_status == "Cancelled":
                    return Response({"error": "Cancelled leave cannot be edited."}, status=400)

                new_date_from_str = data.get("leave_date_from")
                new_date_to_str = data.get("leave_date_to")
                leave.reason = data.get("reason", leave.reason)

                if new_date_from_str or new_date_to_str:
                    try:
                        leave_date_from = (
                            datetime.strptime(new_date_from_str, "%Y-%m-%d").date()
                            if new_date_from_str else leave.leaveDateFrom
                        )
                        leave_date_to = (
                            datetime.strptime(new_date_to_str, "%Y-%m-%d").date()
                            if new_date_to_str else leave.leaveDateTo
                        )
                    except ValueError:
                        return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

                    no_of_days = (leave_date_to - leave_date_from).days + 1
                    if no_of_days <= 0:
                        return Response(
                            {"error": "leave_date_to must be greater than or equal to leave_date_from."},
                            status=400,
                        )

                    overlap = tblleaveapply.objects.filter(
                        empID=employee,
                        leaveDateFrom__lte=leave_date_to,
                        leaveDateTo__gte=leave_date_from,
                    ).exclude(pk=leave.pk).exclude(current_status="Cancelled").exists()
                    if overlap:
                        return Response(
                            {"error": "Leave already applied for some of these dates."},
                            status=400,
                        )

                    nepali_month_count = {}
                    current_date = leave_date_from
                    while current_date <= leave_date_to:
                        nepali_month = nepali_datetime.date.from_datetime_date(current_date).strftime("%B")
                        nepali_month_count[nepali_month] = nepali_month_count.get(nepali_month, 0) + 1
                        current_date += timedelta(days=1)

                    nepali_year, np_from = convert_eng_to_nepali(leave_date_from.strftime("%Y-%m-%d"))
                    _, np_to = convert_eng_to_nepali(leave_date_to.strftime("%Y-%m-%d"))

                    leave.leaveDateFrom = leave_date_from
                    leave.leaveDateTo = leave_date_to
                    leave.noOfDays = no_of_days
                    leave.nepali_month = json.dumps(nepali_month_count)
                    leave.nepali_year = nepali_year
                    leave.leaveDateFrom_np = np_from
                    leave.leaveDateTo_np = np_to

                leave.save()

        except tblleaveapply.DoesNotExist:
            return Response({"error": "Leave application not found."}, status=404)

        # Summaries for every Nepali month the (new) dates touch
        months_touched = []
        day = leave.leaveDateFrom
        while day <= leave.leaveDateTo:
            np_day = nepali_datetime.date.from_datetime_date(day)
            pair = (np_day.year, np_day.strftime("%B"))
            if pair not in months_touched:
                months_touched.append(pair)
            day += timedelta(days=1)

        month_summaries = [
            {"year": year, "month": month, **get_leave_summary(employee, year, month)}
            for year, month in months_touched
        ]

        return Response(
            {
                "message": "Leave application updated successfully.",
                "id": leave.id,
                "leaveDateFrom": leave.leaveDateFrom,
                "leaveDateTo": leave.leaveDateTo,
                "noOfDays": leave.noOfDays,
                "reason": leave.reason,
                "current_status": leave.current_status,
                "month_summaries": month_summaries,
            },
            status=status.HTTP_200_OK,
        )

# class tblleaveapplyStatusUpdateAPIView(APIView):
#     # TODO: restrict to admin/HR permission classes
#     def patch(self, request, pk, *args, **kwargs):
#         new_status = request.data.get("current_status")
#         if new_status not in ALLOWED_LEAVE_STATUSES:
#             return Response(
#                 {"error": f"Invalid current_status. Allowed: {sorted(ALLOWED_LEAVE_STATUSES)}"},
#                 status=400,
#             )

#         try:
#             with transaction.atomic():
#                 leave = tblleaveapply.objects.select_for_update().get(pk=pk)
#                 old_status = leave.current_status
#                 employee = leave.empID

#                 if old_status == new_status:
#                     return Response({"message": "Status unchanged.", "id": leave.id,
#                                      "current_status": old_status}, status=200)

#                 # Coming back from Cancelled: its dates may now clash with another leave
#                 if old_status == "Cancelled":
#                     overlap = tblleaveapply.objects.filter(
#                         empID=employee,
#                         leaveDateFrom__lte=leave.leaveDateTo,
#                         leaveDateTo__gte=leave.leaveDateFrom,
#                     ).exclude(pk=leave.pk).exclude(current_status="Cancelled").exists()
#                     if overlap:
#                         return Response({"error": "Leave already applied for some of these dates but is in Cancelled State"},
#                                         status=400)

#                 paid_record = tblpaidleaves.objects.select_for_update().get(empID=employee)

#                 # Undo the old deduction (only Approved leaves ever deducted)
#                 if old_status == "Approved":
#                     paid_record.no_of_leaves += leave.noOfPaidLeaves_taken

#                 # Recompute the split against the real, current balance
#                 available = paid_record.no_of_leaves
#                 days = Decimal(leave.noOfDays)
#                 if available < days:
#                     paid_taken = available
#                     unpaid_days = days - available
#                     balance_after = Decimal("0")
#                 else:
#                     paid_taken = days
#                     unpaid_days = Decimal("0")
#                     balance_after = available - days

#                 # Apply the new deduction (only Approved deducts)
#                 if new_status == "Approved":
#                     paid_record.no_of_leaves = balance_after

#                 paid_record.save()

#                 leave.current_status = new_status
#                 leave.noOfPaidLeaves = balance_after
#                 leave.noOfUnPaidLeaves = unpaid_days
#                 leave.noOfPaidLeaves_taken = paid_taken
#                 leave.save()

#         except tblleaveapply.DoesNotExist:
#             return Response({"error": "Leave application not found."}, status=404)
#         except tblpaidleaves.DoesNotExist:
#             return Response({"error": "Paid leave record not found for this employee."}, status=404)

#         return Response(
#             {
#                 "message": "Leave status updated successfully.",
#                 "id": leave.id,
#                 "current_status": leave.current_status,
#                 "noOfPaidLeaves": leave.noOfPaidLeaves,
#                 "noOfUnPaidLeaves": leave.noOfUnPaidLeaves,
#                 "noOfPaidLeaves_taken": leave.noOfPaidLeaves_taken,
#                 "current_balance": paid_record.no_of_leaves,
#             },
#             status=status.HTTP_200_OK,
#         )  

from api.serializers.paid_leaves import tblleaveapplySerializer

from datetime import date, datetime


class tblleaveapplyListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        branch_id = request.query_params.get("branchID")
        emp_ID = request.query_params.get("emp_ID")

        if not branch_id:
            return Response(
                {"error": "branchID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        leave_apply = tblleaveapply.objects.select_related("empID")

        # Employee first (if sent), then branch
        if emp_ID:
            try:
                leave_apply = leave_apply.filter(empID__id=int(emp_ID))
            except (ValueError, TypeError):
                return Response(
                    {"error": "emp_ID must be a number."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        leave_apply = leave_apply.filter(empID__branch__id=branch_id)

        date_param = request.query_params.get("date")
        if date_param:
            try:
                from_date = datetime.strptime(date_param, "%Y-%m-%d").date()
            except ValueError:
                return Response(
                    {"error": "Invalid date format. Use YYYY-MM-DD."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # Leaves that end on or after the given date (includes ones in progress on that date)
            leave_apply = leave_apply.filter(leaveDateTo__gte=from_date).order_by("leaveDateFrom")

        leave_serializer = tblleaveapplySerializer(leave_apply, many=True)

        return Response(
            {"leaves_applied": leave_serializer.data},
            status=status.HTTP_200_OK,
        )

# ALLOWED_LEAVE_STATUSES = {"Pending", "Approved", "Cancelled"}
# from decimal import Decimal

# class tblleaveapplyEmployeeCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         data = request.data

#         empID = data.get("empID")
#         if empID is None:
#             return Response({"error": "No employee selected"}, status=400)

#         try:
#             employee = Employee.objects.get(id=int(empID))
#         except (Employee.DoesNotExist, ValueError, TypeError):
#             return Response({"error": "Employee not found"}, status=404)

#         leave_date_from = data.get("leave_date_from")
#         leave_date_to = data.get("leave_date_to")
#         reason = data.get("reason", None)

#         if not leave_date_from or not leave_date_to:
#             return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)

#         # Status comes from the request, defaults to Pending, and must be a known value
#         current_status = data.get("current_status") or "Pending"
#         if current_status not in ALLOWED_LEAVE_STATUSES:
#             return Response(
#                 {"error": f"Invalid current_status. Allowed: {sorted(ALLOWED_LEAVE_STATUSES)}"},
#                 status=400,
#             )

#         # Validate dates BEFORE converting them
#         try:
#             leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
#             leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
#         except ValueError:
#             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

#         no_of_days = (leave_date_to - leave_date_from).days + 1
#         if no_of_days <= 0:
#             return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

#         nepali_year, converted_nepali_date = convert_eng_to_nepali(leave_date_from.strftime("%Y-%m-%d"))
#         _, converted_nepali_date_to = convert_eng_to_nepali(leave_date_to.strftime("%Y-%m-%d"))

#         # Nepali month breakdown
#         nepali_month_count = {}
#         current_date = leave_date_from
#         while current_date <= leave_date_to:
#             nepali_date = nepali_datetime.date.from_datetime_date(current_date)
#             nepali_month = nepali_date.strftime("%B")
#             nepali_month_count[nepali_month] = nepali_month_count.get(nepali_month, 0) + 1
#             current_date += timedelta(days=1)
#         nepali_month_json = json.dumps(nepali_month_count)

#         apply_date = datetime.today().date()

#         try:
#             with transaction.atomic():
#                 # Block overlapping applications (Cancelled ones don't count)
#                 overlap = tblleaveapply.objects.filter(
#                     empID=employee,
#                     leaveDateFrom__lte=leave_date_to,
#                     leaveDateTo__gte=leave_date_from,
#                 ).exclude(current_status="Cancelled").exists()
#                 if overlap:
#                     return Response(
#                         {"error": "Leave already applied for some of these dates."},
#                         status=400,
#                     )

#                 paid_leaves = tblpaidleaves.objects.select_for_update().get(empID=employee)
#                 balance = paid_leaves.no_of_leaves
#                 days = Decimal(no_of_days)

#                 if balance < days:
#                     paid_taken = balance
#                     unpaid_days = days - balance
#                     balance_after = Decimal("0")
#                 else:
#                     paid_taken = days
#                     unpaid_days = Decimal("0")
#                     balance_after = balance - days

#                 # Only deduct the balance when the leave is actually approved
#                 if current_status == "Approved":
#                     paid_leaves.no_of_leaves = balance_after
#                     paid_leaves.save()

#                 leave_apply = tblleaveapply.objects.create(
#                     empID=employee,
#                     applyDate=apply_date,
#                     noOfDays=no_of_days,
#                     leaveDateFrom=leave_date_from,
#                     leaveDateTo=leave_date_to,
#                     reason=reason,
#                     noOfPaidLeaves=balance_after,
#                     noOfUnPaidLeaves=unpaid_days,
#                     nepali_month=nepali_month_json,
#                     nepali_year=nepali_year,
#                     leaveDateFrom_np=converted_nepali_date,
#                     leaveDateTo_np=converted_nepali_date_to,
#                     noOfPaidLeaves_taken=paid_taken,
#                     current_status=current_status,
#                 )
#         except tblpaidleaves.DoesNotExist:
#             return Response({"error": "Paid leave record not found for this employee."}, status=404)

#         response_data = {
#             "id": leave_apply.id,
#             "empID": leave_apply.empID.id,
#             "applyDate": leave_apply.applyDate,
#             "noOfDays": leave_apply.noOfDays,
#             "leaveDateFrom": leave_apply.leaveDateFrom,
#             "leaveDateTo": leave_apply.leaveDateTo,
#             "reason": leave_apply.reason,
#             "noOfPaidLeaves": leave_apply.noOfPaidLeaves,
#             "noOfUnPaidLeaves": leave_apply.noOfUnPaidLeaves,
#             "noOfPaidLeaves_taken": leave_apply.noOfPaidLeaves_taken,
#             "current_status": leave_apply.current_status,
#         }
#         return Response(response_data, status=status.HTTP_201_CREATED)



class tblleaveapplyEmployeeCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        empID = data.get("empID")
        if empID is None:
            return Response({"error": "No employee selected"}, status=400)

        try:
            employee = Employee.objects.get(id=int(empID))
        except (Employee.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Employee not found"}, status=404)

        leave_date_from = data.get("leave_date_from")
        leave_date_to = data.get("leave_date_to")
        reason = data.get("reason", None)

        if not leave_date_from or not leave_date_to:
            return Response({"error": "Both leave_date_from and leave_date_to are required"}, status=400)

        # Status comes from the request, defaults to Pending, and must be a known value
        current_status = data.get("current_status") or "Pending"
        if current_status not in ALLOWED_LEAVE_STATUSES:
            return Response(
                {"error": f"Invalid current_status. Allowed: {sorted(ALLOWED_LEAVE_STATUSES)}"},
                status=400,
            )

        # Validate dates BEFORE converting them
        try:
            leave_date_from = datetime.strptime(leave_date_from, "%Y-%m-%d").date()
            leave_date_to = datetime.strptime(leave_date_to, "%Y-%m-%d").date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)

        no_of_days = (leave_date_to - leave_date_from).days + 1
        if no_of_days <= 0:
            return Response({"error": "leave_date_to must be greater than or equal to leave_date_from."}, status=400)

        nepali_year, converted_nepali_date = convert_eng_to_nepali(leave_date_from.strftime("%Y-%m-%d"))
        _, converted_nepali_date_to = convert_eng_to_nepali(leave_date_to.strftime("%Y-%m-%d"))

        # Nepali month breakdown, plus the (year, month) pairs the leave touches
        nepali_month_count = {}
        months_touched = []
        current_date = leave_date_from
        while current_date <= leave_date_to:
            nepali_date = nepali_datetime.date.from_datetime_date(current_date)
            nepali_month = nepali_date.strftime("%B")
            nepali_month_count[nepali_month] = nepali_month_count.get(nepali_month, 0) + 1
            if (nepali_date.year, nepali_month) not in months_touched:
                months_touched.append((nepali_date.year, nepali_month))
            current_date += timedelta(days=1)
        nepali_month_json = json.dumps(nepali_month_count)

        apply_date = datetime.today().date()

        with transaction.atomic():
            # Lock the employee row so two simultaneous applications can't both pass the overlap check
            Employee.objects.select_for_update().get(pk=employee.pk)

            # Block overlapping applications (Cancelled ones don't count)
            overlap = tblleaveapply.objects.filter(
                empID=employee,
                leaveDateFrom__lte=leave_date_to,
                leaveDateTo__gte=leave_date_from,
            ).exclude(current_status="Cancelled").exists()
            if overlap:
                return Response(
                    {"error": "Leave already applied for some of these dates."},
                    status=400,
                )

            leave_apply = tblleaveapply.objects.create(
                empID=employee,
                applyDate=apply_date,
                noOfDays=no_of_days,
                leaveDateFrom=leave_date_from,
                leaveDateTo=leave_date_to,
                reason=reason,
                nepali_month=nepali_month_json,
                nepali_year=nepali_year,
                leaveDateFrom_np=converted_nepali_date,
                leaveDateTo_np=converted_nepali_date_to,
                current_status=current_status,
            )

        month_summaries = [
            {"year": year, "month": month, **get_leave_summary(employee, year, month)}
            for year, month in months_touched
        ]

        response_data = {
            "id": leave_apply.id,
            "empID": leave_apply.empID.id,
            "applyDate": leave_apply.applyDate,
            "noOfDays": leave_apply.noOfDays,
            "leaveDateFrom": leave_apply.leaveDateFrom,
            "leaveDateTo": leave_apply.leaveDateTo,
            "reason": leave_apply.reason,
            "current_status": leave_apply.current_status,
            "month_summaries": month_summaries,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class tblleaveapplyStatusUpdateAPIView(APIView):
    # TODO: restrict to admin/HR permission classes
    def patch(self, request, pk, *args, **kwargs):
        new_status = request.data.get("current_status")
        if new_status not in ALLOWED_LEAVE_STATUSES:
            return Response(
                {"error": f"Invalid current_status. Allowed: {sorted(ALLOWED_LEAVE_STATUSES)}"},
                status=400,
            )

        try:
            with transaction.atomic():
                leave = tblleaveapply.objects.select_for_update().get(pk=pk)
                employee = leave.empID

                if leave.current_status == new_status:
                    return Response({"message": "Status unchanged.", "id": leave.id,
                                     "current_status": new_status}, status=200)

                # Coming back from Cancelled: its dates may now clash with another leave
                if leave.current_status == "Cancelled":
                    overlap = tblleaveapply.objects.filter(
                        empID=employee,
                        leaveDateFrom__lte=leave.leaveDateTo,
                        leaveDateTo__gte=leave.leaveDateFrom,
                    ).exclude(pk=leave.pk).exclude(current_status="Cancelled").exists()
                    if overlap:
                        return Response(
                            {"error": "Leave already applied for some of these dates."},
                            status=400,
                        )

                leave.current_status = new_status
                leave.save()
        except tblleaveapply.DoesNotExist:
            return Response({"error": "Leave application not found."}, status=404)

        start_np = nepali_datetime.date.from_datetime_date(leave.leaveDateFrom)
        summary = get_leave_summary(employee, start_np.year, start_np.strftime("%B"))

        return Response(
            {
                "message": "Leave status updated successfully.",
                "id": leave.id,
                "current_status": leave.current_status,
                "month_summary": summary,  # for the month the leave starts in
            },
            status=status.HTTP_200_OK,
        )

class tblleaveapplyDeleteAPIView(APIView):
    def delete(self, request, pk, *args, **kwargs):
        try:
            with transaction.atomic():
                leave = tblleaveapply.objects.select_for_update().get(pk=pk)
                paid_leave_record = tblpaidleaves.objects.select_for_update().get(empID=leave.empID)
                paid_leave_record.no_of_leaves += leave.noOfPaidLeaves_taken
                paid_leave_record.save()
                leave.delete()
        except tblleaveapply.DoesNotExist:
            return Response({"error": "Leave application not found."}, status=404)
        except tblpaidleaves.DoesNotExist:
            return Response({"error": "Paid leave record not found for this employee."}, status=404)

        return Response(
            {"message": "Leave application deleted and paid leave balance restored."},
            status=status.HTTP_200_OK,
        )

        
from employee.models import tblpaidleaves
class GetEmploeeNoofPaidLeavesApiView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        employee = data.get("emp_ID", None)

        try:
            employee = Employee.objects.get(id=int(employee))

        except Exception as e:
            return Response({"error": "No employee found"}, 400)
        
        # employee_paidleaves = tblpaidleaves.objects.get(empID=employee)

        # no_of_days = employee_paidleaves.no_of_leaves

        from organization.models import Branch

        branch  = Branch.objects.first()
        no_of_days = branch.noOfpaidleavesallowed



        return Response({"paidleaves": no_of_days}, 200)
        

        
        
class tblleaveapplyCancelAPIView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data


        tblleaveapply_id  = data.get("id", None)
        try:
            tblleaveapply_obj = tblleaveapply.objects.get(id=int(tblleaveapply_id))
        
        except Exception as e:
            return Response({"error": "No leave apply found of that id"}, 400)
        empID = tblleaveapply_obj.empID.id
        if tblleaveapply_obj.current_status == "Cancelled":
            return Response({"error": "Leave is already in the cancelled state"}, 400)           

        noOfPaidLeaves_taken = tblleaveapply_obj.noOfPaidLeaves_taken

        if noOfPaidLeaves_taken != 0.0:
            employee_tblpaidleaves_obj = tblpaidleaves.objects.get(empID__id = int(empID))
            employee_tblpaidleaves_obj.no_of_leaves += noOfPaidLeaves_taken
            employee_tblpaidleaves_obj.save()

        tblleaveapply_obj.current_status = "Cancelled"
        tblleaveapply_obj.save()

        return Response({"detail": "Leave cancelled successfully"}, status=status.HTTP_201_CREATED)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from api.serializers.paid_leaves import tblpaidleavesSerializer
# from api.models import tblpaidleaves  # Ensure you import your model

class GetEmployeePaidLeaves(APIView):
    def get(self, request, *args, **kwargs):
        # Retrieve all records from the tblpaidleaves table
        employees_paidleaves = tblpaidleaves.objects.all()
        
        # Serialize the queryset (note the many=True argument)
        serializer = tblpaidleavesSerializer(employees_paidleaves, many=True)
        
        # Get the serialized data
        data = serializer.data
        
        # Return the response with the serialized data
        return Response(data, status=200)
