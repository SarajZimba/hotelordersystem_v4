from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from user.models import Customer
from ..serializers.user import CustomTokenPairSerializer, CustomerSerializer

from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenPairSerializer


class CustomerAPI(ModelViewSet):
    serializer_class = CustomerSerializer
    model = Customer
    queryset = Customer.objects.active()
    pagination_class = None

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from api.serializers.user import AgentSerializer
from django.contrib.auth.models import Group


class AgentViewSet(viewsets.ViewSet):
    serializer_class = AgentSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            usercode = serializer.validated_data['username']
            full_name = serializer.validated_data['full_name']

            user = User.objects.create(username=usercode, full_name=full_name, is_superuser=False, is_staff=True)

            user.set_password(usercode)
            user.save()

            group = Group.objects.get(name="agent")
            user.groups.add(group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
        
            return Response({"detail":"User with the username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
from rest_framework import generics
# from .models import Customer
# from .serializers import CustomerSerializer

class CustomerDetailAPIView(generics.RetrieveAPIView):
    serializer_class = CustomerSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Customer.objects.active()  # Ensure you have the correct queryset
    
from rest_framework import generics
# from .models import Customer
# from .serializers import CustomerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class CustomerListAPIView(APIView):

    def get(self, request):

        customers = Customer.objects.filter(is_deleted=False)
        serializer = CustomerSerializer(customers, many=True)
        return Response (serializer.data, 200)  # Ensure you have the correct queryset

from api.serializers.user import AdminSerializer
class AdminViewSet(viewsets.ViewSet):
    serializer_class = AdminSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            usercode = serializer.validated_data['username']
            full_name = serializer.validated_data['full_name']
            password = serializer.validated_data['password']

            user = User.objects.create(username=usercode, full_name=full_name, is_superuser=False, is_staff=True)

            user.set_password(password)
            from organization.models import Organization

            organization = Organization.objects.first()

            user.organization = organization
            user.save()

            group = Group.objects.get(name="admin")
            user.groups.add(group)



            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"detail": "User with the username or email already exists"}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class AdminDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        if not username:
            return Response({"detail": "username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"detail": f"User '{username}' not found."}, status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            # UserBranchAccess.objects.filter(user=user).delete()
            user.delete()

        return Response(
            {"detail": f"User '{username}' and associated branch access deleted successfully."},
            status=status.HTTP_200_OK,
        )

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction


class AdminUpdateView(APIView):

    def post(self, request):
        data = request.data

        current_username = data.get('username')
        new_username = data.get('new_username')
        password = data.get('password')

        if not current_username:
            return Response({"detail": "username is required."}, status=status.HTTP_400_BAD_REQUEST)

        if not new_username and not password:
            return Response({"detail": "No fields provided to update."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=current_username)
        except User.DoesNotExist:
            return Response({"detail": f"User '{current_username}' not found."}, status=status.HTTP_404_NOT_FOUND)

        if new_username and new_username != current_username:
            if User.objects.filter(username=new_username).exists():
                return Response({"detail": f"Username '{new_username}' already exists."}, status=status.HTTP_409_CONFLICT)

        with transaction.atomic():
            if new_username:
                user.username = new_username
            if password:
                user.set_password(password)
            user.save()

        return Response({
            "detail": "User updated successfully.",
            "username": user.username
        }, status=status.HTTP_200_OK)