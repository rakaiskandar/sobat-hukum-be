from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.permissions import IsAdminUser
from .models import Cases
from api.users.models import Lawyers, Clients
from .serializers import CaseSerializer
from rest_framework.permissions import IsAuthenticated
from api.common.permissions import IsAdminPermission

class CaseViewSet(APIView):
    queryset = Cases.objects.all()  # Semua data kasus
    serializer_class = CaseSerializer
    permission_classes = [IsAuthenticated, IsAdminPermission]

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
        data['client_id'] = client.client_id  # Set client_id berdasarkan user yang login
        data['created_by'] = user.name
        data['user_id'] = user.user_id
        # Validasi dan simpan data menggunakan serializer
        serializer = CaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()  # Simpan data ke database
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ApproveCaseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, case_id):
        user = request.user

        # Cek apakah user adalah lawyer
        if not hasattr(user, 'lawyer'):
            return Response({"message": "Only lawyers can approve cases."}, status=403)

        # Ambil kasus berdasarkan case_id
        try:
            case = Cases.objects.get(case_id=case_id)
        except Cases.DoesNotExist:
            return Response({"message": "Case not found."}, status=404)

        # Jika kasus sudah memiliki lawyer_id yang berbeda
        if case.lawyer_id is not None:
            if str(case.lawyer_id.lawyer_id) != str(user.lawyer.lawyer_id):  # Bandingkan lawyer_id dalam bentuk string
                return Response({
                    "message": "This case is already assigned to another lawyer.",
                    "case_lawyer_id": str(case.lawyer_id.lawyer_id),  # Konversi ke string
                    "your_lawyer_id": str(user.lawyer.lawyer_id)  # Konversi ke string
                }, status=403)

            # Jika lawyer_id cocok, ubah status ke approved
            case.status = "approved"
            case.save()
            return Response({"message": f"Case {case.case_id} approved successfully by lawyer {user.lawyer.lawyer_id}."}, status=200)

        # Jika kasus tidak memiliki lawyer_id, assign ke lawyer yang meng-approve
        case.lawyer_id = user.lawyer  # Assign instance dari Lawyers, bukan string
        case.status = "approved"
        case.save()
        return Response({
            "message": f"Case {case.case_id} approved successfully and assigned to lawyer {user.lawyer.lawyer_id}.",
            "case_id": case.case_id,
            "lawyer_id": str(case.lawyer_id.lawyer_id)  # Konversi ke string
        }, status=200)

class OpenCasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Query untuk kasus dengan lawyer_id kosong
        open_cases = Cases.objects.filter(lawyer_id=None)
        if open_cases.exists():
            serializer = CaseSerializer(open_cases, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No cases available without a lawyer."}, status=200)
        
class CasesAssignView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Query untuk kasus dengan lawyer_id kosong
        lawyer_id = request.user.lawyer.lawyer_id

        # Query untuk kasus dengan lawyer_id sesuai
        assigned_cases = Cases.objects.filter(lawyer_id=lawyer_id)

        if assigned_cases.exists():
            serializer = CaseSerializer(assigned_cases, many=True)
            return Response(serializer.data, status=200)
        else:
            return Response({"message": "No cases assigned to you."}, status=200)
        
class DeleteCaseView(APIView):
    permission_classes = [IsAdminPermission]  # Gunakan custom permission

    def delete(self, request, case_id):
        try:
            # Cari kasus berdasarkan case_id
            case = Cases.objects.get(case_id=case_id)
            case.delete()
            return Response(
                {"message": f"Case {case_id} has been successfully deleted."},
                status=status.HTTP_200_OK,
            )
        except Cases.DoesNotExist:
            return Response({"error": "Case not found."}, status=status.HTTP_404_NOT_FOUND)

class ListAllCasesView(APIView):
    permission_classes = [IsAdminPermission]  # Hanya admin yang dapat mengakses

    def get(self, request):
        try:
            # Ambil semua kasus dari database
            cases = Cases.objects.all()

            # Serialisasi data
            serializer = CaseSerializer(cases, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": "An error occurred while fetching cases.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )