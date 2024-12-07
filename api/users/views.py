from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, LoginSerializer, ClientSerializer, LawyerSerializer
from .models import Clients, Lawyers
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

        is_verified = None
        if user.role == "client":
            client = Clients.objects.get(user=user.user_id)
            is_verified = client.is_verified
        elif user.role == "lawyer":
            lawyer = Lawyers.objects.get(user=user.user_id)
            is_verified = lawyer.is_verified
        else:
            is_verified = True
            
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
                "is_verified": is_verified,
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
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    http_method_names = ['post']  # Only allow POST

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