from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .permissions import IsAdminPermission
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer, LoginSerializer
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
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                "token": token.key,
                "username": user.username,
                "role": user.role,  # Tambahkan role di respons
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdminPermission]

    def get(self, request):
        return Response({"message": "You are an admin!"})