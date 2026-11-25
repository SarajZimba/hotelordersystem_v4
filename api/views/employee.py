# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from employee.models import Employee
# from api.serializers.employee import EmployeeSerializer

# class EmployeeGetAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             employees = Employee.objects.all()

#             serializer = EmployeeSerializer(employees, many=True)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# class EmployeeCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# class EmployeeDetailAPIView(APIView):
    
#     def get_object(self, pk):
#         try:
#             return Employee.objects.get(pk=pk)
#         except Employee.DoesNotExist:
#             return Response({"detail":"Employee not found"}, status=status.HTTP_400_BAD_REQUEST)

#     def patch(self, request, pk, *args, **kwargs):
#         # Get the employee object by the provided ID (primary key)
#         employee = self.get_object(pk)
        
#         # Pass the updated data to the serializer, including the existing instance
#         serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        
#         # Check if the data is valid
#         if serializer.is_valid():
#             serializer.save()  # Save the changes to the instance
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk, *args, **kwargs):
#         # Get the employee object by the provided ID (primary key)
#         employee = self.get_object(pk)
        
#         # Delete the employee instance
#         employee.delete()
#         return Response({"detail": "employee deleted successfully"},status=status.HTTP_200_OK)
        
        
# from api.serializers.employee import DailyAttendanceSerializer

# # class DailyAttendanceCreateAPIView(APIView):
# #     def post(self, request, *args, **kwargs):
# #         # Create a serializer instance with the incoming data
# #         serializer = DailyAttendanceSerializer(data=request.data)
        
# #         # Check if the data is valid
# #         if serializer.is_valid():
# #             # Save the new DailyAttendance record
# #             serializer.save()
# #             # Return the serialized data with a 201 Created status
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
        
# #         # If data is invalid, return the errors with a 400 Bad Request status
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # from datetime import datetime

# # class DailyAttendanceCreateAPIView(APIView):
# #     def post(self, request, *args, **kwargs):

# #         data = request.data


# #         today_date = datetime.today().date()

# #         # Get the current time for check-in
# #         current_time = datetime.now().time()

# #         empID = data.get('empID', None)
# #         # time = data.get('time', None)

# #         if empID == None:
# #             return Response({"detail": "Please provide a employee Id"}, 400)
        
# #         employee = Employee.objects.get(id=int(empID))

# #         # check for check-in 

# #         if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
# #             employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
            
# #             # Check if the employee has already checked out
# #             # if employees_dailyattendance.check_out is not None:
# #             #     return Response({"detail": "Employee has already checked out."}, 400)
# #             employees_dailyattendance.check_out = current_time
# #             employees_dailyattendance.save()

# #             return Response({"detail": "Check out time recorded successfully"}, 200)

# #         else:
# #             create_data = {
# #                           "attendance_date":today_date,
# #                           "check_in":current_time,
# #                           "empID":int(empID)}
# #             # Create a serializer instance with the incoming data
# #             serializer = DailyAttendanceSerializer(data=create_data)

# #             # Check if the data is valid
# #             if serializer.is_valid():
# #                 # Save the new DailyAttendance record
# #                 serializer.save()
# #                 # Return the serialized data with a 201 Created status
# #                 return Response(serializer.data, status=status.HTTP_201_CREATED)
            
# #             # If data is invalid, return the errors with a 400 Bad Request status
# #             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from api.serializers.employee import DailyAttendanceSerializer

# from datetime import datetime

# class DailyAttendanceCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):

#         data = request.data


#         today_date = datetime.today().date()

#         # Get the current time for check-in
#         current_time = datetime.now().time()

#         empID = data.get('empID', None)
#         # time = data.get('time', None)

#         if empID == None:
#             return Response({"detail": "Please provide a employee Id"}, 400)
        
#         employee = Employee.objects.get(id=int(empID))

#         # check for check-in 

#         if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#             employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)

#             # Check if the employee has already checked out
#             # if employees_dailyattendance.check_out is not None:
#             #     return Response({"detail": "Employee has already checked out."}, 400)
#             employees_dailyattendance.check_out = current_time
#             # Calculate the total time worked
#             if employees_dailyattendance.check_in is not None:
#                 check_in_time = datetime.combine(employees_dailyattendance.attendance_date, employees_dailyattendance.check_in)
#                 check_out_time = datetime.combine(employees_dailyattendance.attendance_date, current_time)
#                 total_time = check_out_time - check_in_time
#                 employees_dailyattendance.total_time = (datetime.min + total_time).time()  # Convert timedelta to time

#             employees_dailyattendance.save()

#             return Response({"detail": "Check out time recorded successfully"}, 200)

#         if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#             employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
#             employees_dailyattendance.check_out = current_time
#             employees_dailyattendance.save()

#             return Response({"detail": "Check out time recorded successfully"}, 200)

#         else:
#             create_data = {
#                           "attendance_date":today_date,
#                           "check_in":current_time,
#                           "empID":int(empID)}
#             # Create a serializer instance with the incoming data
#             serializer = DailyAttendanceSerializer(data=create_data)

#             # Check if the data is valid
#             if serializer.is_valid():
#                 # Save the new DailyAttendance record
#                 serializer.save()
#                 # Return the serialized data with a 201 Created status
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
            
#             # If data is invalid, return the errors with a 400 Bad Request status
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# from employee.models import DailyAttendance


# class DailyAttendanceDetailAPIView(APIView):
    
#     # Helper method to get the DailyAttendance object
#     def get_object(self, pk):
#         try:
#             return DailyAttendance.objects.get(pk=pk)
#         except DailyAttendance.DoesNotExist:
#             return Response({"detail":"Daily Attendance not found"}, status=status.HTTP_400_BAD_REQUEST)

#     # PATCH method to partially update a DailyAttendance record
#     def patch(self, request, pk, *args, **kwargs):
#         # Retrieve the DailyAttendance record
#         attendance = self.get_object(pk)
        
#         # Create the serializer with the existing attendance and the updated data
#         serializer = DailyAttendanceSerializer(attendance, data=request.data, partial=True)
        
#         # Check if the data is valid
#         if serializer.is_valid():
#             serializer.save()  # Save the updated data
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         # If data is invalid, return validation errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # DELETE method to delete a DailyAttendance record
#     def delete(self, request, pk, *args, **kwargs):
#         # Retrieve the DailyAttendance record
#         attendance = self.get_object(pk)
        
#         # Delete the record
#         attendance.delete()
#         return Response({"detail": "Attendance deleted successfully"}, status=status.HTTP_200_OK)
        
# class EmployeesDailyAttendanceGetAPIView(APIView):
#     """
#     API view to retrieve daily attendance for a specific employee.
#     """

#     def post(self, request, *args, **kwargs):
#         try:
#             # Validate input data
#             data = request.data
#             employee_id = data.get('employee')

#             if not employee_id:
#                 return Response({"detail": "Please provide an employee ID."}, status=status.HTTP_400_BAD_REQUEST)

#             # Fetch attendance records
#             employees_attendance = DailyAttendance.objects.filter(empID__id=int(employee_id))
            
#             if not employees_attendance.exists():
#                 return Response({"detail": "No attendance records found for the given employee."}, status=status.HTTP_404_NOT_FOUND)

#             # Serialize and return data
#             serializer = DailyAttendanceSerializer(employees_attendance, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except ValueError:
#             return Response({"detail": "Invalid employee ID provided."}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
# from api.serializers.employee import PayPackageSerializer
# class PayPackageCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PayPackageSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
# class SearchEmployeeAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         try:
#             data = request.data

#             employee_id = data['emp_id']
#             employees = Employee.objects.get(id=int(employee_id))

#             serializer = EmployeeSerializer(employees)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
# class GetCheckinOutStatus(APIView):
#     def get(self, request, *args, **kwargs):

#         today_date = datetime.today().date()

#         employees = Employee.objects.filter(current_status="Enrolled", attendance_required=True)

#         if employees:
#             employees_list = []
#             for employee in employees:

#                 if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#                     dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
#                     response_data = {
#                         "check-in": True,
#                         "check-in-time": dailyattendance.check_in,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name,
#                         "total_time": dailyattendance.total_time,
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,
#                     }

#                     if dailyattendance.check_out is not None:
#                         response_data["check-out"] = True
#                         response_data["check-out-time"] = dailyattendance.check_out
#                 else:
#                     response_data = {
#                         "check-in": False,
#                         "check-in-time": None,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name, 
#                         "total_time": None,
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,
#                     }
#                 employees_list.append(response_data)
#             return Response(employees_list, 200)
#         else:
#             return Response("no active employees found", 400)
            
# class GetAllDailyAttendance(APIView):
#     def get(self, request, *args, **kwargs):

#         today_date = datetime.today().date()

#         employees = Employee.objects.all()

#         if employees:
#             employees_list = []
#             for employee in employees:

#                 if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
#                     dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
#                     response_data = {
#                         "check-in": True,
#                         "check-in-time": dailyattendance.check_in,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name,
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,
#                     }

#                     if dailyattendance.check_out is not None:
#                         response_data["check-out"] = True
#                         response_data["check-out-time"] = dailyattendance.check_out
#                 else:
#                     response_data = {
#                         "check-in": False,
#                         "check-in-time": None,
#                         "check-out": False,
#                         "check-out-time": None,
#                         "employee_id": employee.id,
#                         "employee_name": employee.name,    
#                         "branch_name": employee.branch.name if employee.branch else None,
#                         "branch_id": employee.branch.id if employee.branch else None,
#                         "level": employee.level,
#                         "shift": employee.shift,
#                         "attendance_required": employee.attendance_required,
#                         "lateattendance_alert": employee.lateattendance_alert,             
#                     }
#                 employees_list.append(response_data)
#             return Response(employees_list, 200)
#         else:
#             return Response("no active employees found", 400)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from employee.models import Employee
from api.serializers.employee import EmployeeSerializer
from employee.models import tblpaidleaves
from organization.models import Organization


# class EmployeeGetAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             employees = Employee.objects.all()

#             serializer = EmployeeSerializer(employees, many=True)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

# class EmployeeGetAPIView(APIView):
#     def get(self, request, *args, **kwargs):
#         try:
#             today_date = datetime.today().date()
#             employees = Employee.objects.filter(current_status="Enrolled")

#             serializer = EmployeeSerializer(employees, many=True)

#             employees_count = Employee.objects.filter(current_status="Enrolled").count()

#             enrolled_employees = Employee.objects.all()
#             married_employees_count = enrolled_employees.filter(marital_status="Married").count()
#             unmarried_employees_count = enrolled_employees.filter(marital_status="Unmarried").count()
#             divorced_employees_count = enrolled_employees.filter(marital_status="Divorced").count()
#             male_employees_count = enrolled_employees.filter(gender="male").count()
#             female_employees_count = enrolled_employees.filter(gender="female").count()
#             # Check if the employee is on leave today
#             # count_employees_on_leave = tblleaveapply.objects.filter(
#             #         leaveDateFrom__lte=today_date,
#             #         leaveDateTo__gte=today_date,
#             #         current_status = "Approved"
#             #     ).count()
#             # no_of_approved_leaves = tblleaveapply.objects.filter(
#             #         current_status = "Approved"
#             #     ).count()
#             # no_of_pending_leaves = tblleaveapply.objects.filter(
#             #         current_status = None
#             #     ).count()
            
            
#             response_data = {
#                 "employees" : serializer.data,
#                 "employees_count" : employees_count,
#                 "married" :married_employees_count,
#                 "unmarried" :unmarried_employees_count,
#                 "divorced" :divorced_employees_count,
#                 "male" :male_employees_count,
#                 "female" :female_employees_count
#                 # "on_leave" :count_employees_on_leave,
#                 # "approved_leaves" :no_of_approved_leaves,
#                 # "pending_leaves" :no_of_pending_leaves,
#             }
            
#             return Response(response_data, status=status.HTTP_201_CREATED)
#         except Exception as e:
#             return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

class EmployeeGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            branch_id = request.query_params.get("branch")

            employees_qs = Employee.objects.all()
            if branch_id:
                employees_qs = employees_qs.filter(branch_id=branch_id)

            # enrolled_employees = employees_qs.filter(current_status="Enrolled")
            enrolled_employees = employees_qs

            serializer = EmployeeSerializer(enrolled_employees, many=True)

            employees_count = enrolled_employees.count()

            # NOTE: "enrolled_employees" name below is misleading in the original code —
            # it actually queried ALL employees regardless of status, not just enrolled ones.
            # Keeping that same scope here (branch-filtered), just renamed for clarity.
            all_branch_employees = employees_qs
            married_employees_count = all_branch_employees.filter(marital_status="Married").count()
            unmarried_employees_count = all_branch_employees.filter(marital_status="Unmarried").count()
            divorced_employees_count = all_branch_employees.filter(marital_status="Divorced").count()
            male_employees_count = all_branch_employees.filter(gender="male").count()
            female_employees_count = all_branch_employees.filter(gender="female").count()

            response_data = {
                "employees": serializer.data,
                "employees_count": employees_count,
                "married": married_employees_count,
                "unmarried": unmarried_employees_count,
                "divorced": divorced_employees_count,
                "male": male_employees_count,
                "female": female_employees_count,
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            
class AllEmployeeGetAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            today_date = datetime.today().date()
            employees = Employee.objects.all()

            serializer = EmployeeSerializer(employees, many=True)

            employees_count = Employee.objects.all().count()

            enrolled_employees = Employee.objects.all()
            married_employees_count = enrolled_employees.filter(marital_status="Married").count()
            unmarried_employees_count = enrolled_employees.filter(marital_status="Unmarried").count()
            divorced_employees_count = enrolled_employees.filter(marital_status="Divorced").count()
            male_employees_count = enrolled_employees.filter(gender="male").count()
            female_employees_count = enrolled_employees.filter(gender="female").count()
            # Check if the employee is on leave today
                                                                                                 
            
            
            response_data = {
                "employees" : serializer.data,
                "employees_count" : employees_count,
                "married" :married_employees_count,
                "unmarried" :unmarried_employees_count,
                "divorced" :divorced_employees_count,
                "male" :male_employees_count,
                "female" :female_employees_count
            }
            
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)

        
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404

User = get_user_model()           
            
from api.serializers.employee import EmployeePayPackageSerializer

# class EmployeeCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         from organization.models import Branch

#         branch_id = request.data.get("branch")
#         if not branch_id:
#             return Response({"branch": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             branch = Branch.objects.get(id=branch_id)
#         except Branch.DoesNotExist:
#             return Response({"branch": "Invalid branch id."}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = EmployeeSerializer(data=request.data)
#         if serializer.is_valid():
#             employee_instance = serializer.save()
#             tblpaidleaves.objects.create(empID=employee_instance, no_of_leaves=branch.noOfpaidleavesallowed)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EmployeeCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         from organization.models import Branch

#         branch_id = request.data.get("branch")
#         if not branch_id:
#             return Response({"branch": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             branch = Branch.objects.get(id=branch_id)
#         except Branch.DoesNotExist:
#             return Response({"branch": "Invalid branch id."}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = EmployeeSerializer(data=request.data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         username = serializer.validated_data["username"]
#         if User.objects.filter(username=username).exists():
#             return Response(
#                 {"username": "A user with this username already exists."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         try:
#             with transaction.atomic():
#                 employee_instance = serializer.save()
#                 tblpaidleaves.objects.create(
#                     empID=employee_instance,
#                     no_of_leaves=branch.noOfpaidleavesallowed,
#                 )

#                 user = User(
#                     username=username,
#                     full_name=employee_instance.name,
#                     is_superuser=False,
#                     is_staff=True,
#                 )
#                 user.password = employee_instance.password  # already hashed by the serializer
#                 user.save()
#                 user.groups.add(Group.objects.get(name="agent"))

#         except Group.DoesNotExist:
#             return Response(
#                 {"detail": "User group 'agent' does not exist."},
#                 status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             )
#         except IntegrityError:
#             return Response(
#                 {"username": "A user with this username already exists."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         return Response(serializer.data, status=status.HTTP_201_CREATED)


class EmployeeCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        from organization.models import Branch

        branch_id = request.data.get("branch")
        if not branch_id:
            return Response({"branch": "This field is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            branch = Branch.objects.get(id=branch_id)
        except Branch.DoesNotExist:
            return Response({"branch": "Invalid branch id."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EmployeeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]  # plain text, as stored on Employee

        if User.objects.filter(username=username).exists():
            return Response(
                {"username": "A user with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            with transaction.atomic():
                employee_instance = serializer.save()
                tblpaidleaves.objects.create(
                    empID=employee_instance,
                    no_of_leaves=branch.noOfpaidleavesallowed,
                )

                user = User(
                    username=username,
                    full_name=employee_instance.name,
                    is_superuser=False,
                    is_staff=True,
                )
                user.set_password(password)  # the User table always stores a hash
                user.save()
                user.groups.add(Group.objects.get(name="agent"))

        except Group.DoesNotExist:
            return Response(
                {"detail": "User group 'agent' does not exist."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except IntegrityError:
            return Response(
                {"username": "A user with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class SearchEmployeeAPIView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            employee_id = data['emp_id']
            employees = Employee.objects.get(id=int(employee_id))

            serializer = EmployeePayPackageSerializer(employees)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
        
class GetCheckinOutStatus(APIView):
    def get(self, request, *args, **kwargs):

        today_date = datetime.today().date()

        employees = Employee.objects.filter(current_status="Enrolled", attendance_required=True)

        if employees:
            employees_list = []
            for employee in employees:

                if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
                    dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee, empID__attendance_required=True)
                    response_data = {
                        "check-in": True,
                        "check-in-time": dailyattendance.check_in,
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": employee.lateattendance_alert,
                    }

                    if dailyattendance.check_out is not None:
                        response_data["check-out"] = True
                        response_data["check-out-time"] = dailyattendance.check_out
                else:
                    response_data = {
                        "check-in": False,
                        "check-in-time": None,
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,    
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": employee.lateattendance_alert,             
                    }
                employees_list.append(response_data)
            return Response(employees_list, 200)
        else:
            return Response("no active employees found", 400)




from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


# class EmployeeDetailAPIView(APIView):
#     # permission_classes = [IsAuthenticated, IsHR]  # restrict who can edit/delete

#     def get_object(self, pk):
#         return get_object_or_404(Employee, pk=pk)

#     def get(self, request, pk, *args, **kwargs):
#         serializer = EmployeeSerializer(self.get_object(pk))
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def patch(self, request, pk, *args, **kwargs):
#         employee = self.get_object(pk)
#         serializer = EmployeeSerializer(employee, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def delete(self, request, pk, *args, **kwargs):
#         employee = self.get_object(pk)
#         employee.delete()
#         return Response(
#             {"detail": "Employee deleted successfully"},
#             status=status.HTTP_200_OK,
#         )
    



class EmployeeDetailAPIView(APIView):
    # permission_classes = [IsAuthenticated, IsHR]  # restrict who can edit/delete

    def get_object(self, pk):
        return get_object_or_404(Employee, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        serializer = EmployeeSerializer(self.get_object(pk))
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk, *args, **kwargs):
        employee = self.get_object(pk)
        old_username = employee.username
        new_username = request.data.get("username")
        raw_password = request.data.get("password")

        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # The login that belongs to this employee (found by the username before the edit).
        # Superusers are never touched.
        linked_user = (
            User.objects.filter(username=old_username, is_superuser=False).first()
            if old_username else None
        )

        # The new username must be free in the User table, ignoring this employee's own user
        if new_username and new_username != old_username:
            clash = User.objects.filter(username=new_username)
            if linked_user:
                clash = clash.exclude(pk=linked_user.pk)
            if clash.exists():
                return Response(
                    {"username": "A user with this username already exists."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        try:
            with transaction.atomic():
                employee = serializer.save()
                self._sync_user(employee, linked_user, raw_password)
        except Group.DoesNotExist:
            return Response(
                {"detail": "User group 'agent' does not exist."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except IntegrityError:
            return Response(
                {"username": "A user with this username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(serializer.data, status=status.HTTP_200_OK)

    # def _sync_user(self, employee, user, raw_password):
    #     if user is None:
    #         # Employee created before logins existed: create the user now
    #         if not employee.username or not employee.password:
    #             return
    #         user = User(
    #             username=employee.username,
    #             full_name=employee.name,
    #             is_superuser=False,
    #             is_staff=True,
    #         )
    #         user.password = employee.password  # already hashed by the serializer
    #         user.save()
    #         user.groups.add(Group.objects.get(name="agent"))
    #         return

    def _sync_user(self, employee, user, raw_password):
        if user is None:
            # Employee with no login yet: create it only if a password was sent now
            if not employee.username or not raw_password:
                return
            user = User(
                username=employee.username,
                full_name=employee.name,
                is_superuser=False,
                is_staff=True,
            )
            user.set_password(raw_password)  # the User table always stores a hash
            user.save()
            user.groups.add(Group.objects.get(name="agent"))
            return

        user.username = employee.username
        user.full_name = employee.name
        if raw_password:
            user.set_password(raw_password)
        user.save()

        user.username = employee.username
        user.full_name = employee.name
        if raw_password:
            user.set_password(raw_password)
        user.save()

    def delete(self, request, pk, *args, **kwargs):
        employee = self.get_object(pk)
        with transaction.atomic():
            if employee.username:
                # Deactivate instead of deleting, so records linked to the user are kept
                User.objects.filter(username=employee.username, is_superuser=False).update(is_active=False)
            employee.delete()
        return Response(
            {"detail": "Employee deleted successfully"},
            status=status.HTTP_200_OK,
        )

from api.serializers.employee import DailyAttendanceSerializer

from datetime import datetime, timedelta
from organization.models import Organization

class DailyAttendanceCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):

        data = request.data

        org = Organization.objects.first()

        arrival_time = org.arrival_time

        today_date = datetime.today().date()

        # Get the current time for check-in
        current_time = datetime.now().time()

        empID = data.get('empID', None)
        # time = data.get('time', None)

        if empID == None:
            return Response({"detail": "Please provide a employee Id"}, 400)
        
        employee = Employee.objects.get(id=int(empID))
        
        # Convert arrival_time and current_time to datetime for comparison
        today_datetime = datetime.combine(today_date, arrival_time)
        current_datetime = datetime.combine(today_date, current_time)

        late_attendance_flag = False
        no_show_flag = False


        # # Check if current time is more than 30 minutes after arrival time
        # if current_datetime > today_datetime + timedelta(minutes=30):
        #     no_show_flag = True
        if current_datetime > today_datetime:
            if current_datetime <= today_datetime + timedelta(minutes=15):
                print(current_datetime)
                print(today_datetime)
                late_attendance_flag = False
                no_show_flag = False
            else:
                late_attendance_flag = True
                no_show_flag = False
            # Check if current time is within 15 minutes of arrival time

        # else:

        #     late_attendance_flag = False
        #     no_show_flag = False

        # check for check-in 

        if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
            employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)

            # Check if the employee has already checked out
            # if employees_dailyattendance.check_out is not None:
            #     return Response({"detail": "Employee has already checked out."}, 400)
            employees_dailyattendance.check_out = current_time
            # Calculate the total time worked
            if employees_dailyattendance.check_in is not None:
                check_in_time = datetime.combine(employees_dailyattendance.attendance_date, employees_dailyattendance.check_in)
                check_out_time = datetime.combine(employees_dailyattendance.attendance_date, current_time)
                total_time = check_out_time - check_in_time
                employees_dailyattendance.total_time = (datetime.min + total_time).time()  # Convert timedelta to time

            employees_dailyattendance.save()

            return Response({"detail": "Check out time recorded successfully"}, 200)

        # if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
        #     employees_dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
        #     employees_dailyattendance.check_out = current_time
        #     employees_dailyattendance.save()

        #     return Response({"detail": "Check out time recorded successfully"}, 200)

        else:
            create_data = {
                           "attendance_date":today_date,
                           "check_in":current_time,
                           "empID":int(empID),
                            "late_attendance_flag" : late_attendance_flag,
                            "no_show_flag": no_show_flag}
            # Create a serializer instance with the incoming data
            serializer = DailyAttendanceSerializer(data=create_data)

            # Check if the data is valid
            if serializer.is_valid():
                # Save the new DailyAttendance record
                serializer.save()
                # Return the serialized data with a 201 Created status
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            # If data is invalid, return the errors with a 400 Bad Request status
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
from employee.models import DailyAttendance


class DailyAttendanceDetailAPIView(APIView):
    
    # Helper method to get the DailyAttendance object
    def get_object(self, pk):
        try:
            return DailyAttendance.objects.get(pk=pk)
        except DailyAttendance.DoesNotExist:
            return Response({"detail":"Daily Attendance not found"}, status=status.HTTP_400_BAD_REQUEST)

    # PATCH method to partially update a DailyAttendance record
    def patch(self, request, pk, *args, **kwargs):
        # Retrieve the DailyAttendance record
        attendance = self.get_object(pk)
        
        # Create the serializer with the existing attendance and the updated data with partial=True which will only update the fields sent
        serializer = DailyAttendanceSerializer(attendance, data=request.data, partial=True)
        
        # Check if the data is valid
        if serializer.is_valid():
            serializer.save()  # Save the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # If data is invalid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE method to delete a DailyAttendance record
    def delete(self, request, pk, *args, **kwargs):
        # Retrieve the DailyAttendance record
        attendance = self.get_object(pk)
        
        # Delete the record
        attendance.delete()
        return Response({"detail": "Attendance deleted successfully"}, status=status.HTTP_200_OK)

class EmployeesDailyAttendanceGetAPIView(APIView):
    """
    API view to retrieve daily attendance for a specific employee.
    """

    def post(self, request, *args, **kwargs):
        try:
            # Validate input data
            data = request.data
            employee_id = data.get('employee')

            if not employee_id:
                return Response({"detail": "Please provide an employee ID."}, status=status.HTTP_400_BAD_REQUEST)

            # Fetch attendance records
            employees_attendance = DailyAttendance.objects.filter(empID__id=int(employee_id))
            
            if not employees_attendance.exists():
                return Response({"detail": "No attendance records found for the given employee."}, status=status.HTTP_404_NOT_FOUND)

            # Serialize and return data
            serializer = DailyAttendanceSerializer(employees_attendance, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError:
            return Response({"detail": "Invalid employee ID provided."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# from api.serializers.employee import PayPackageSerializer
# class PayPackageCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         serializer = PayPackageSerializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from api.serializers.employee import PayPackageSerializer
# from decimal import Decimal
# from employee.models import tblEmployeeSalary
# class PayPackageCreateAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         posted_data = request.data
#         serializer = PayPackageSerializer(data=posted_data, many=True)


#         if serializer.is_valid():
#             serializer.save()

#             total = Decimal(0.0)
#             taxable = Decimal(0.0)
#             non_taxable = Decimal(0.0)
#             for data in posted_data:
#                 total += Decimal(data["amount"])
#                 if data["taxable"]:
#                     taxable += Decimal(data["amount"])
#                 else:
#                     non_taxable += Decimal(data["amount"])

#             empID = posted_data[0]["empID"]

#             employee = Employee.objects.get(id=int(empID))

#             if tblEmployeeSalary.objects.filter(emp_ID=employee).exists():
#                 employee_salaryobj = tblEmployeeSalary.objects.get(emp_ID=employee)
#                 employee_salaryobj.total_salary += total
#                 employee_salaryobj.taxable += taxable
#                 employee_salaryobj.non_taxable += non_taxable
#                 employee_salaryobj.save()
#             else:
#                 tblEmployeeSalary.objects.create(emp_ID=employee, total_salary=total, taxable=taxable, non_taxable=non_taxable)

#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.db import transaction
from decimal import Decimal
from employee.models import tblEmployeeSalary, MasterPayPackage
from api.serializers.employee import PayPackageSerializer


class PayPackageCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        posted_data = request.data

        if not isinstance(posted_data, list) or len(posted_data) == 0:
            return Response(
                {"error": "Expected a non-empty list of pay package objects."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for idx, item in enumerate(posted_data):
            if "empID" not in item:
                return Response({"error": f"Item {idx}: 'empID' is required."}, status=status.HTTP_400_BAD_REQUEST)
            if "package" not in item:
                return Response({"error": f"Item {idx}: 'package' is required."}, status=status.HTTP_400_BAD_REQUEST)
            if "amount" not in item:
                return Response({"error": f"Item {idx}: 'amount' is required."}, status=status.HTTP_400_BAD_REQUEST)

        empID = posted_data[0]["empID"]
        if any(item["empID"] != empID for item in posted_data):
            return Response(
                {"error": "All pay package items must belong to the same empID."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = Employee.objects.get(id=int(empID))
        except (Employee.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid empID."}, status=status.HTTP_400_BAD_REQUEST)

        # fetch all referenced MasterPayPackage rows in one query, so we know
        # each package's taxable status without hitting the DB per item
        package_ids = [item["package"] for item in posted_data]
        master_packages = {
            mp.id: mp for mp in MasterPayPackage.objects.filter(id__in=package_ids)
        }
        missing = set(package_ids) - set(master_packages.keys())
        if missing:
            return Response(
                {"error": f"Invalid package id(s): {sorted(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PayPackageSerializer(data=posted_data, many=True)

        if serializer.is_valid():
            try:
                with transaction.atomic():
                    serializer.save()

                    total = Decimal("0.0")
                    taxable_total = Decimal("0.0")
                    non_taxable_total = Decimal("0.0")

                    for item in posted_data:
                        amount = Decimal(str(item["amount"]))
                        total += amount
                        master = master_packages[item["package"]]
                        if master.taxable:
                            taxable_total += amount
                        else:
                            non_taxable_total += amount

                    employee_salaryobj, created = tblEmployeeSalary.objects.get_or_create(
                        emp_ID=employee,
                        defaults={
                            "total_salary": total,
                            "taxable": taxable_total,
                            "non_taxable": non_taxable_total,
                        }
                    )
                    if not created:
                        employee_salaryobj.total_salary += total
                        employee_salaryobj.taxable += taxable_total
                        employee_salaryobj.non_taxable += non_taxable_total
                        employee_salaryobj.save()
            except Exception as e:
                return Response({"error": f"Failed to save pay package: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from employee.models import tblleaveapply
class GetAllDailyAttendance(APIView):
    def get(self, request, *args, **kwargs):

        today_date = datetime.today().date()

        employees = Employee.objects.filter(current_status="Enrolled", attendance_required=True)

        count_employees_on_leave = tblleaveapply.objects.filter(
                    empID__current_status = "Enrolled",
                    leaveDateFrom__lte=today_date,
                    leaveDateTo__gte=today_date,
                    current_status = "Approved"
                ).count()
        no_of_approved_leaves = tblleaveapply.objects.filter(
                    current_status = "Approved",empID__current_status = "Enrolled"
                ).count()
        no_of_pending_leaves = tblleaveapply.objects.filter(
                    current_status = None,empID__current_status = "Enrolled"
                ).count()
        # late_attendance_flag = models.BooleanField(null=True)
        # no_show_flag = models.BooleanField(null=True)
        no_of_late_arrival = DailyAttendance.objects.filter(late_attendance_flag=True, attendance_date=today_date, empID__current_status="Enrolled", empID__attendance_required=True).count()
        # no_show= DailyAttendance.objects.filter(no_show_flag=True, attendance_date=today_date, empID__current_status="Enrolled", empID__attendance_required=True).count()

        if employees:
            employees_list = []
            for employee in employees:
                # Check if the employee is on leave today
                on_leave = tblleaveapply.objects.filter(
                    empID=employee,
                    leaveDateFrom__lte=today_date,
                    leaveDateTo__gte=today_date,
                    current_status = "Approved"
                ).exists()
                if DailyAttendance.objects.filter(attendance_date=today_date, empID= employee).exists():
                    dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)
                    response_data = {
                        "check-in": True,
                        "check-in-time": dailyattendance.check_in.strftime('%I:%M %p'),
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": dailyattendance.late_attendance_flag,
                        "no_show": dailyattendance.no_show_flag,
                        "type": employee.type,
                        "leave": on_leave  # Add leave status to response

                    }

                    if dailyattendance.check_out is not None:
                        response_data["check-out"] = True
                        response_data["check-out-time"] = dailyattendance.check_out.strftime('%I:%M %p')
                else:
                    # dailyattendance = DailyAttendance.objects.get(attendance_date=today_date, empID=employee)

                    if on_leave:
                        no_show = False
                    else:
                        org = Organization.objects.last()
                        arrival_time = org.arrival_time
                        today_date = datetime.today().date()
                        
                        # Get the current time for check-in
                        current_time = datetime.now().time()
                        
                        # Convert arrival_time and current_time to datetime for comparison
                        today_datetime = datetime.combine(today_date, arrival_time)
                        current_datetime = datetime.combine(today_date, current_time)
                        no_show = True


                        # # Check if current time is more than 30 minutes after arrival time
                        # if current_datetime > today_datetime + timedelta(minutes=30):
                        #     no_show_flag = True
                        if current_datetime > today_datetime:
                            if current_datetime <= today_datetime + timedelta(minutes=30):
                                no_show= False
                            else:
                                no_show=True
                        else:
                            no_show=False

                    response_data = {
                        "check-in": False,
                        "check-in-time": None,
                        "check-out": False,
                        "check-out-time": None,
                        "employee_id": employee.id,
                        "employee_name": employee.name,    
                        "branch_name": employee.branch.name if employee.branch else None,
                        "branch_id": employee.branch.id if employee.branch else None,
                        "level": employee.level,
                        "shift": employee.shift,
                        "attendance_required": employee.attendance_required,
                        "lateattendance_alert": False,
                        "no_show": no_show,
                        "type": employee.type,
                        "leave": on_leave  # Add leave status to response

                    }
                employees_list.append(response_data)
            no_of_employees = employees.count()
            no_show= DailyAttendance.objects.filter(attendance_date=today_date,empID__current_status="Enrolled", no_show_flag=False, empID__attendance_required=True).count()
            no_of_on_leave = tblleaveapply.objects.filter(
                        leaveDateFrom__lte=today_date,
                        leaveDateTo__gte=today_date,
                        current_status = "Approved",
                        empID__current_status="Enrolled",
                        empID__attendance_required=True
                    ).count()
    
            no_of_no_show = sum(employee["no_show"] for employee in employees_list) 
            response_data = {
                "employee_list" : employees_list,
                "on_leave" :count_employees_on_leave,
                "approved_leaves" :no_of_approved_leaves,
                "pending_leaves" :no_of_pending_leaves,
                "no_of_late_arrival" : no_of_late_arrival,
                "no_show": no_of_no_show,
                "arrival_time" : Organization.objects.first().arrival_time,
                "clock_out_time" : Organization.objects.first().clock_out_time
            }
            return Response(response_data, 200)
        else:
            return Response("no active employees found", 400)
    
from employee.models import Pay_Package
class RemovePayPackage(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        package_id = data.get('package_id', None)

        if package_id is None:
            return Response({"error": "The package id cannot be Null"}, 400)
        try:
            package = Pay_Package.objects.get(id=int(package_id))
        except Exception as e:
            return Response({"error": "No package found of that passed Id"}, 400)

        package.delete()

        return Response({"detail":"Package has been removed successfully"}, 200)

from api.serializers.employee import MasterPayPackageSerializer
from decimal import Decimal
from employee.models import MasterPayPackage


class MasterPayPackageListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        branch_id = request.query_params.get("branch")

        packages = MasterPayPackage.objects.all()
        if branch_id:
            packages = packages.filter(branch__id=branch_id)

        serializer = MasterPayPackageSerializer(packages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        posted_data = request.data
        package_name = posted_data.get("package_name")
        branch_id = posted_data.get("branch")

        if package_name:
            duplicate = MasterPayPackage.objects.filter(
                package_name__iexact=package_name.strip(),
                branch=branch_id
            )
            if duplicate.exists():
                return Response(
                    {"error": f"A pay package named '{package_name}' already exists for this branch."},
                    status=status.HTTP_400_BAD_REQUEST
                )

        serializer = MasterPayPackageSerializer(data=posted_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404


class MasterPayPackageDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(MasterPayPackage, pk=pk)

    def get(self, request, pk, *args, **kwargs):
        package = self.get_object(pk)
        serializer = MasterPayPackageSerializer(package)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def _update(self, request, pk, partial):
        package = self.get_object(pk)
        posted_data = request.data

        # Use the new values if sent, otherwise fall back to the current ones
        package_name = posted_data.get("package_name", package.package_name)
        branch_id = posted_data.get("branch", package.branch_id)

        if package_name:
            duplicate = MasterPayPackage.objects.filter(
                package_name__iexact=package_name.strip(),
                branch_id=branch_id,
            ).exclude(pk=package.pk)  # don't clash with itself
            if duplicate.exists():
                return Response(
                    {"error": f"A pay package named '{package_name}' already exists for this branch."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = MasterPayPackageSerializer(package, data=posted_data, partial=partial)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        return self._update(request, pk, partial=False)

    def patch(self, request, pk, *args, **kwargs):
        return self._update(request, pk, partial=True)

    def delete(self, request, pk, *args, **kwargs):
        package = self.get_object(pk)
        try:
            package.delete()
        except ProtectedError:
            return Response(
                {"error": "This pay package is in use and cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)

    
from api.views.salary_sheet import get_monthly_equivalent
class EmployeePayPackageListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        emp_id = request.query_params.get("empID")
        if not emp_id:
            return Response({"error": "empID is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employee_obj = Employee.objects.get(id=int(emp_id))
        except (Employee.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid empID."}, status=status.HTTP_400_BAD_REQUEST)

        pay_packages = Pay_Package.objects.filter(empID=employee_obj).select_related("package")

        result = []
        for pp in pay_packages:
            result.append({
                "id": pp.id,
                "amount": pp.amount,
                "monthly_equivalent": get_monthly_equivalent(pp),  # reuse existing helper
                "package_id": pp.package.id if pp.package else None,
                "package_name": pp.package.package_name if pp.package else None,
                "package_type": pp.package.package_type if pp.package else None,
                "taxable": pp.package.taxable if pp.package else None,
            })

        return Response({
            "empID": employee_obj.id,
            "name": employee_obj.name,
            "pay_packages": result,
        }, status=status.HTTP_200_OK)

    
from decimal import Decimal, InvalidOperation
class EmployeePayPackageDetailAPIView(APIView):
    """
    PUT: Edit a specific Pay_Package's amount/package assignment.
    DELETE: Remove a specific Pay_Package assignment from an employee.
    URL: /employeepaypackage/<int:pk>/
    """

    def put(self, request, pk, *args, **kwargs):
        try:
            pay_package = Pay_Package.objects.get(id=pk)
        except (Pay_Package.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid pay package id."}, status=status.HTTP_400_BAD_REQUEST)

        data = request.data

        amount = data.get("amount")
        if amount is not None:
            try:
                pay_package.amount = Decimal(str(amount))
            except (InvalidOperation, ValueError, TypeError):
                return Response({"error": "Invalid amount."}, status=status.HTTP_400_BAD_REQUEST)

        package_id = data.get("package")
        if package_id is not None:
            try:
                master_package = MasterPayPackage.objects.get(id=package_id)
            except (MasterPayPackage.DoesNotExist, ValueError, TypeError):
                return Response({"error": "Invalid package id."}, status=status.HTTP_400_BAD_REQUEST)

            # prevent duplicate: employee already has this package under a different row
            if Pay_Package.objects.filter(
                empID=pay_package.empID, package=master_package
            ).exclude(id=pay_package.id).exists():
                return Response(
                    {"error": "This package is already assigned to this employee under another record."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            pay_package.package = master_package

        pay_package.save()

        return Response({
            "id": pay_package.id,
            "empID": pay_package.empID_id,
            "amount": pay_package.amount,
            "package_id": pay_package.package.id if pay_package.package else None,
            "package_name": pay_package.package.package_name if pay_package.package else None,
            "package_type": pay_package.package.package_type if pay_package.package else None,
        }, status=status.HTTP_200_OK)

    def delete(self, request, pk, *args, **kwargs):
        try:
            pay_package = Pay_Package.objects.get(id=pk)
        except (Pay_Package.DoesNotExist, ValueError, TypeError):
            return Response({"error": "Invalid pay package id."}, status=status.HTTP_400_BAD_REQUEST)

        package_name = pay_package.package.package_name if pay_package.package else None
        emp_id = pay_package.empID_id

        pay_package.delete()

        return Response({
            "message": "Pay package removed successfully.",
            "empID": emp_id,
            "removed_package": package_name,
        }, status=status.HTTP_200_OK)

class CheckinTime(APIView):
    def get(self, request, *args, **kwargs):
        org = Organization.objects.first()

        if org is None:
            return Response({"No organization found", 400})
        arrival_time = org.arrival_time

        return Response({"arrival_time": arrival_time}, 200)
        
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models import tblEmployeeCIT
from api.serializers.employee import tblEmployeeCITSerializer

class EmployeeCITAPI(APIView):
    def get(self, request):
        """Fetch all Employee CIT records."""
        employees = tblEmployeeCIT.objects.all()
        serializer = tblEmployeeCITSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Create multiple Employee CIT records."""
        if isinstance(request.data, list):  # If multiple objects are posted
            serializer = tblEmployeeCITSerializer(data=request.data, many=True)
        else:  # If a single object is posted
            serializer = tblEmployeeCITSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from employee.models import tblEmployeeCIT
from api.serializers.employee import tblEmployeeCITSerializer

class UpdateEmployeeCITAPI(APIView):
    def put(self, request, pk):
        """Update an Employee CIT record."""
        try:
            employee_cit = tblEmployeeCIT.objects.get(id=pk)
        except tblEmployeeCIT.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = tblEmployeeCITSerializer(employee_cit, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteEmployeeCITAPI(APIView):
    def delete(self, request, pk):
        """Delete an Employee CIT record."""
        try:
            employee_cit = tblEmployeeCIT.objects.get(id=pk)
        except tblEmployeeCIT.DoesNotExist:
            return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)

        employee_cit.delete()
        return Response({"detail": "Record deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


from datetime import date, datetime


class DailyAttendanceSummaryAPIView(APIView):
    """
    Query params: branchID (required), date (optional, YYYY-MM-DD, defaults to today)
    present = enrolled employees - employees on approved leave that day
    attendance_rate = present / enrolled employees * 100
    """
    def get(self, request, *args, **kwargs):
        branch_id = request.query_params.get("branchID")
        if not branch_id:
            return Response(
                {"error": "branchID is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        date_param = request.query_params.get("date")
        try:
            target_date = (
                datetime.strptime(date_param, "%Y-%m-%d").date()
                if date_param else date.today()
            )
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employees = Employee.objects.filter(branch_id=branch_id, current_status="Enrolled")
        total_employees = employees.count()

        # Distinct employees with an approved leave covering the target date
        on_leave_ids = set(
            tblleaveapply.objects.filter(
                empID__in=employees,
                current_status="Approved",
                is_deleted=False,
                leaveDateFrom__lte=target_date,
                leaveDateTo__gte=target_date,
            ).values_list("empID_id", flat=True)
        )

        on_leave_count = len(on_leave_ids)
        present_count = total_employees - on_leave_count
        attendance_rate = (
            round(present_count / total_employees * 100, 2) if total_employees else 0.0
        )

        return Response({
            "branchID": int(branch_id),
            "date": target_date,
            "total_employees": total_employees,
            "on_leave": on_leave_count,
            "present": present_count,
            "attendance_rate": attendance_rate,
            "employees_on_leave": list(
                employees.filter(id__in=on_leave_ids).values("id", "name")
            ),
        }, status=status.HTTP_200_OK)


from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView


class EmployeeLoginThrottle(AnonRateThrottle):
    scope = "employee_login"
    rate = "10/min"  # per IP, slows down password guessing


class EmployeeLoginAPIView(APIView):
    authentication_classes = []  # login must be reachable without credentials
    permission_classes = []
    throttle_classes = [EmployeeLoginThrottle]

    def post(self, request, *args, **kwargs):
        username = (request.data.get("username") or "").strip()
        password = request.data.get("password") or ""

        if not username or not password:
            return Response(
                {"detail": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        employee = (
            Employee.objects
            .filter(username=username, is_deleted=False, current_status="Enrolled")
            .select_related("branch")
            .first()
        )

        # Same message for unknown user, wrong password, or inactive employee,
        # so the response doesn't reveal which usernames exist.
        if employee is None:
            return Response(
                {"detail": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        data = EmployeeSerializer(employee, context={"request": request}).data
        return Response(
            {"message": "Login successful.", "employee": data},
            status=status.HTTP_200_OK,
        )