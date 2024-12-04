from django.db import models
from api.cases.models import Cases  # Import model Cases dari file yang berbeda
from api.common.utils import generate_unique_id

class Documents(models.Model):
    document_id = models.CharField(primary_key=True, default=generate_unique_id, editable=False, max_length=8, unique=True)
    case_id = models.ForeignKey(
        Cases,
        on_delete=models.CASCADE,
        related_name='document'  # related_name yang sesuai untuk akses dari model Cases
    )
    file_name = models.CharField(max_length=255)  # Nama file
    file_path = models.FileField(upload_to='documents/')  # Path file dengan folder penyimpanan 'documents'
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Tanggal dan waktu saat file diunggah

    def __str__(self):
        return self.file_name

class CasesUpdate(models.Model):
    case_update_id = models.CharField(primary_key=True, default=generate_unique_id, editable=False, max_length=8, unique=True)
    document_id = models.ForeignKey(
        Documents,
        on_delete=models.CASCADE,
        related_name='updates'  # related_name untuk akses dari model Documents
    )
    update_detail = models.TextField()  # Detail pembaruan
    updated_at = models.DateTimeField(auto_now_add=True)  # Waktu saat pembaruan dibuat
    status = models.CharField(
        max_length=20,
        choices=[
            ('open', 'Open'),
            ('pending', 'Pending'),
            ('closed', 'Closed'),
            ('on-progress', 'On Progress')
        ],
        default='open'  # Status default adalah 'open'
    )

    def __str__(self):
        return f"Update for {self.document.file_name} - {self.status}"