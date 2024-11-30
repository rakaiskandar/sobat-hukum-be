from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Cases
from api.users.models import Lawyers, Clients
from .serializers import CaseSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdminOrReadOnly

class CaseViewSet(APIView):
    queryset = Cases.objects.all()  # Semua data kasus
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    # Filtering kasus berdasarkan status
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.query_params.get('status')  # Filter berdasarkan query param
        if status:
            queryset = queryset.filter(status=status)
        return queryset

class CreateCaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user

        # Periksa apakah user memiliki role client
        if user.role != 'client':
            return Response({'detail': 'You are not authorized to add cases.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Periksa apakah user terhubung ke data client
        try:
            client = user.client
        except AttributeError:
            return Response({'detail': 'No client profile found for the user.'}, status=status.HTTP_400_BAD_REQUEST)

        # Ambil data dari request
        data = request.data.copy()
        data['client_id'] = client.id  # Set client_id berdasarkan user yang login
        
        # Validasi dan simpan data menggunakan serializer
        serializer = CaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Simpan data ke database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)