from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, ClientSerializer, LawyerSerializer
from .models import Clients, Lawyers
from api.common.permissions import IsAdminPermission
import logging
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

        # is_verified = None
        # if user.role == "client":
        #     client = Clients.objects.get(user=user.user_id)
        #     is_verified = client.is_verified
        # elif user.role == "lawyer":
        #     lawyer = Lawyers.objects.get(user=user.user_id)
        #     is_verified = lawyer.is_verified
        # else:
        #     is_verified = True
            
        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.user_id,
                "name": user.name,
                "username": user.username,
                "profile": user.profile_picture,
                "email": user.email,
                "role": user.role,
                # "is_verified": is_verified,
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

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({'username': user.username, 'role': user.role})

class CreateClientView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'client':
            return Response({'detail': 'You are not authorized to add client data.'}, status=status.HTTP_403_FORBIDDEN)

        # Hapus 'is_verified' dari data yang diinput oleh klien
        data = request.data.copy()
        data.pop('is_verified', None)

        serializer = ClientSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)  # Tautkan data ke user yang login
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyClientView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]  # Hanya admin yang bisa mengakses

    def patch(self, request, client_id):
        try:
            client = Clients.objects.get(client_id=client_id)
        except Clients.DoesNotExist:
            return Response({'detail': 'Client not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifikasi client
        client.is_verified = True
        client.save()

        return Response({'detail': f'Client {client_id} verified successfully.'}, status=status.HTTP_200_OK)

    
class CreateLawyerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'lawyer':
            return Response({'detail': 'You are not authorized to add lawyer data.'}, status=status.HTTP_403_FORBIDDEN)

        # Hapus 'is_verified' dari data yang diinput oleh pengacara
        data = request.data.copy()
        data.pop('is_verified', None)

        serializer = LawyerSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)  # Tautkan data ke user yang login
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyLawyerView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]  # Hanya admin yang bisa mengakses

    def patch(self, request, lawyer_id):
        try:
            lawyer = Lawyers.objects.get(lawyer_id=lawyer_id)
        except Lawyers.DoesNotExist:
            return Response({'detail': 'Lawyer not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Verifikasi lawyer
        lawyer.is_verified = True
        lawyer.save()

        return Response({'detail': f'Lawyer {lawyer_id} verified successfully.'}, status=status.HTTP_200_OK)

class GetClientDetailsByUserIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Ambil user_id dari user yang sedang login
            user = request.user
            client = Clients.objects.get(user=user)  # Cari client berdasarkan user
            return Response(
                {
                    "client_id": client.client_id,
                    "nik": client.nik,
                    "is_verified": client.is_verified,
                },
                status=status.HTTP_200_OK,
            )
        except Clients.DoesNotExist:
            return Response({"error": "Client not found for the provided user"}, status=status.HTTP_404_NOT_FOUND)


class GetLawyerDetailsByUserIdView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # Ambil user_id dari user yang sedang login
            user = request.user
            lawyer = Lawyers.objects.get(user=user)  # Cari lawyer berdasarkan user
            return Response(
                {
                    "lawyer_id": lawyer.lawyer_id,
                    "licence_number": lawyer.licence_number,
                    "specialization": lawyer.specialization,
                    "experience_years": lawyer.experience_years,
                    "is_verified": lawyer.is_verified,
                },
                status=status.HTTP_200_OK,
            )
        except Lawyers.DoesNotExist:
            return Response({"error": "Lawyer not found for the provided user"}, status=status.HTTP_404_NOT_FOUND)