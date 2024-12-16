from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Documents
from api.cases.models import Cases  # Pastikan model Cases diimpor
from .serializers import *
from rest_framework import generics, status

class DocumentViewSet(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Ambil file dan case_id dari request
            file = request.FILES.get('file')
            case_id = request.data.get('case_id')

            # Validasi input
            if not file or not case_id:
                return Response(
                    {"error": "File and Case ID are required"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Ambil instance dari Cases berdasarkan case_id
            try:
                case_instance = Cases.objects.get(case_id=case_id)  # Ambil instance
            except Cases.DoesNotExist:
                return Response(
                    {"error": "Invalid Case ID"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Buat instance Documents
            document = Documents.objects.create(
                case_id=case_instance,  # Tetapkan instance Cases ke case_id
                file_name=file.name,
                file_path=file,
            )

            # Serialisasi dan kirim respons
            serializer = DocumentSerializer(document)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(f"Internal Server Error: {e}")
            return Response(
                {"error": "An internal server error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class DocumentByCaseView(generics.ListAPIView):
    serializer_class = DocumentSerializer

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return Documents.objects.filter(case_id=case_id)

# View untuk menampilkan CaseDetail berdasarkan case_id
class CaseDetailView(generics.ListAPIView):
    serializer_class = CaseDetailSerializer

    def get_queryset(self):
        case_id = self.kwargs['case_id']
        return Documents.objects.filter(case_id=case_id)

# View untuk membuat CaseUpdate
class CreateCaseUpdateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Ambil document_id dari request
            document_id = request.data.get('document_id')
            if not document_id:
                return Response({"error": "document_id is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Validasi keberadaan document
            document = Documents.objects.get(document_id=document_id)

            # Data untuk serializer
            data = {
                'document_id': document.document_id,  # Gunakan instance document
                'update_detail': request.data.get('update_detail'),
                'status': request.data.get('status', 'open'),  # Default status jika tidak disediakan
            }

            serializer = CaseUpdateSerializer(data=data)
            if serializer.is_valid():
                serializer.save()  # Simpan pembaruan
                return Response(
                    {"message": "Case update created successfully", "data": serializer.data},
                    status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Documents.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
