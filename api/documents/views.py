from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Documents
from api.cases.models import Cases  # Pastikan model Cases diimpor
from .serializers import DocumentSerializer

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
