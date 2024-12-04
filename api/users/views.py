from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from api.common.permissions import IsAdminPermission
from .serializers import RegisterSerializer, LoginSerializer, ClientSerializer, LawyerSerializer
from .models import Clients, Lawyers, Users
import logging
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    http_method_names = ['post']  # Hanya izinkan POST

    def post(self, request, *args, **kwargs):
        logger.debug(f"Request data: {request.data}")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
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

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "id": user.user_id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
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

# class AdminOnlyView(APIView):
#     permission_classes = [IsAuthenticated, IsAdminPermission]

#     def get(self, request):
#         return Response({"message": "You are an admin!"})

class CreateClientView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'client':
            return Response({'detail': 'You are not authorized to add client data.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Tautkan data ke user yang login
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateLawyerView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        if user.role != 'lawyer':
            return Response({'detail': 'You are not authorized to add lawyer data.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = LawyerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)  # Tautkan data ke user yang login
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)