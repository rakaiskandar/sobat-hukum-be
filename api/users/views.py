from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import *
from .models import Clients, Lawyers, Users
from django.db.models import Case, When, Value, BooleanField
from api.common.permissions import IsAdminPermission
from rest_framework.parsers import MultiPartParser, FormParser
import logging
from django.utils.encoding import smart_str  
from django.db.models import Count

logger = logging.getLogger(__name__)
from django.db import transaction  # Ensure atomic operations

class RegisterView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']  # Only allow POST

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        transaction.set_rollback(True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']  # Hanya izinkan POST
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
            
        is_verified = None
        if user.role == "client":
            try:
                client = Clients.objects.get(user_id=user.user_id)
                is_verified = client.is_verified
            except Clients.DoesNotExist:
                is_verified = False  # Default behavior for unregistered clients
        elif user.role == "lawyer":
            try:
                lawyer = Lawyers.objects.get(user_id=user.user_id)
                is_verified = lawyer.is_verified
            except Lawyers.DoesNotExist:
                is_verified = False  
        elif user.role == "admin":
            is_verified = True
        
        profile_picture_url = user.profile_picture.url if user.profile_picture else None
         
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.user_id,
                "name": user.name,
                "username": user.username,
                "profile_picture": profile_picture_url,
                "email": user.email,
                "role": user.role,
                "is_verified": is_verified
            },
        }, status=status.HTTP_200_OK)

class VerifyTokenView(APIView):
    """
    Endpoint to verify if an access token is valid.
    """
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        token = request.data.get("token")

        if not token:
            return Response({"detail": "Token is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode the token to verify its validity
            AccessToken(token)
            return Response({"detail": "Token is valid."}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"detail": str(e)}, status=401)

class CreateClientView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    http_method_names = ['post']
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        logger.debug(f"Request data for client: {request.data}")

        # Add the user to the request data
        client_data = request.data.copy()
        client_data['user'] = request.user.user_id
        serializer = ClientSerializer(data=client_data)

        if serializer.is_valid():
            # Save the client and link it to the authenticated user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        transaction.set_rollback(True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyClientView(APIView):
    permission_classes = [IsAdminPermission]  # Hanya admin yang bisa mengakses
    http_method_names = ["patch"]
    
    @transaction.atomic
    def patch(self, request, user_id):
        try:
            client = Clients.objects.get(user_id=user_id)
        except Clients.DoesNotExist:
            transaction.set_rollback(True)
            transaction.set_rollback(True)
            return Response({'detail': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifikasi client
        client.is_verified = True
        client.save()

        return Response({'detail': f'Client {user_id} verified successfully.'}, status=status.HTTP_200_OK)
    
class CreateLawyerView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    http_method_names = ['post']  # Only allow POST
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        logger.debug(f"Request data for lawyer: {request.data}")
        # Add the user to the request data
        lawyer_data = request.data.copy()
        lawyer_data['user'] = request.user.user_id
        serializer = LawyerSerializer(data=lawyer_data)

        if serializer.is_valid():
            # Save the client and link it to the authenticated user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        transaction.set_rollback(True)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyLawyerView(APIView):
    permission_classes = [IsAdminPermission]  # Hanya admin yang bisa mengakses
    http_method_names = ["patch"]
    
    @transaction.atomic
    def patch(self, request, user_id):
        try:
            lawyer = Lawyers.objects.get(user_id=user_id)
        except Lawyers.DoesNotExist:
            transaction.set_rollback(True)
            transaction.set_rollback(True)
            return Response({'detail': 'Lawyer not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifikasi lawyer
        lawyer.is_verified = True
        lawyer.save()

        return Response({'detail': f'Lawyer {user_id} verified successfully.'}, status=status.HTTP_200_OK)

class GetUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]
    
    def get(self, request):
        try:
            # Query the users excluding admins and prefetch related models
            users = Users.objects.exclude(role="admin").prefetch_related('lawyer', 'client')

            # Annotate the `is_verified` field based on the related models
            users = users.annotate(
                is_verified=Case(
                    When(role="client", client__is_verified=True, then=Value(True)),
                    When(role="lawyer", lawyer__is_verified=True, then=Value(True)),
                    default=Value(False),
                    output_field=BooleanField(),
                )
            )
            
            # Serialize the users
            serializer = UserSerializer(users, many=True)
            
            # Return the serialized data
            return Response(serializer.data, status=200)
        
        except Exception as e:
            # Log the exception if needed for debugging purposes
            return Response({"error": str(e)}, status=500)
        
class GetUserMeView(APIView):
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]
    
    def get(self, request):
        try:
            # Fetch the current user's details
            user = Users.objects.prefetch_related('lawyer', 'client').get(user_id=request.user.user_id)

            # Annotate the `is_verified` field:
            # - Admin users are always considered verified.
            # - Otherwise, it depends on the associated client or lawyer model.
            user.is_verified = (
                True if user.role == "admin" else 
                getattr(user.client, 'is_verified', False) if user.role == "client" else
                getattr(user.lawyer, 'is_verified', False) if user.role == "lawyer" else False
            )

            # Prepare role-based data
            role_based_data = {}
            if user.role == "client" and hasattr(user, "client"):
                role_based_data = {
                    "nik": user.client.nik,
                    "is_verified": user.client.is_verified,
                    "client_id": user.client.client_id,
                }
            elif user.role == "lawyer" and hasattr(user, "lawyer"):
                role_based_data = {
                    "license_number": user.lawyer.license_number,
                    "specialization": user.lawyer.specialization,
                    "experience_years": user.lawyer.experience_years,
                    "is_verified": user.lawyer.is_verified,
                    "lawyer_id": user.lawyer.lawyer_id,
                }

            # Serialize the base user data
            serializer = UserSerializer(user)
            user_data = serializer.data

            # Merge role-based data into the serialized response
            response_data = {
                **user_data,
                **role_based_data,
            }

            # Return serialized user profile
            return Response(response_data, status=200)
        
        except Exception as e:
        # Log unexpected exceptions and return 500
            return Response({"error": str(e)}, status=500)

class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    http_method_names = ["patch"]

    def patch(self, request):
        try:
            user = request.user
            
             # If the request contains a profile picture, we need to update it
            user_data = request.data.copy()

            # Only update profile_picture if it's provided in the request
            if 'profile_picture' in user_data:
                # If the 'profile_picture' is set to 'null' or is empty, retain the existing one
                if user_data['profile_picture'] == 'null' or not user_data['profile_picture']:
                    user_data['profile_picture'] = user.profile_picture
                
            # Update user fields
            user_serializer = UpdateUserSerializer(user, data=request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()

                # Handle role-specific updates
                if user.role == "client":
                    client = user.client
                    client_serializer = UpdateClientSerializer(client, data=request.data, partial=True)
                    if client_serializer.is_valid():
                        client_serializer.save()
                    else:
                        return Response(client_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                elif user.role == "lawyer":
                    lawyer = user.lawyer
                    lawyer_serializer = UpdateLawyerSerializer(lawyer, data=request.data, partial=True)
                    if lawyer_serializer.is_valid():
                        lawyer_serializer.save()
                    else:
                        return Response(lawyer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # Include role-specific data in response
                response_data = user_serializer.data
                if user.role == "client":
                    response_data["client_data"] = client_serializer.data
                elif user.role == "lawyer":
                    response_data["lawyer_data"] = lawyer_serializer.data

                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class LawyerListPublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            lawyers = Lawyers.objects.select_related('user').filter(experience_years__gt=5).all()  # Filter lawyers dengan pengalaman lebih dari 5 tahun
            data = [
                {
                    "lawyer_id": lawyer.lawyer_id,
                    "profile_picture": lawyer.user.profile_picture.url if lawyer.user.profile_picture else None,
                    "name": smart_str(lawyer.user.name, encoding='utf-8'),
                    "email": smart_str(lawyer.user.email, encoding='utf-8'),
                    "specialization": smart_str(lawyer.specialization, encoding='utf-8'),
                }
                for lawyer in lawyers
            ]
            return Response(data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class LawyerListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Ambil semua data lawyer dengan user terkait
        try:
            lawyers = Lawyers.objects.select_related('user').all()
            data = [
                {
                    "lawyer_id": lawyer.lawyer_id,
                    "profile_picture": lawyer.user.profile_picture.url if lawyer.user.profile_picture else None,
                    "name": smart_str(lawyer.user.name, encoding='utf-8'),
                    "email": smart_str(lawyer.user.email, encoding='utf-8'),
                    "specialization": smart_str(lawyer.specialization, encoding='utf-8'),
                }
                for lawyer in lawyers
            ]
            return Response(data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=500)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]  # Hanya untuk user yang sudah login

    def get(self, request, user_id):
        try:
            # Ambil user berdasarkan user_id
            user = Users.objects.get(user_id=user_id)
            serializer = UserDetailSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response({"error": "User tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)

class UserCountView(APIView):
    permission_classes = [IsAdminPermission]

    def get(self, request):
        try:
            # Count the number of users with role 'lawyer' and 'client'
            user_counts = (
                Users.objects.filter(role__in=["lawyer", "client"])  # Filter for lawyer and client roles
                .values("role")  # Group by role field
                .annotate(count=Count("user_id"))  # Count users for each role
            )

            # Prepare the data to only include lawyer and client
            formatted_data = []
            for role in ["lawyer", "client"]:
                count = next((entry["count"] for entry in user_counts if entry["role"] == role), 0)
                formatted_data.append({"role": role.capitalize(), "count": count})

            return Response(formatted_data, status=200)
        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=500)