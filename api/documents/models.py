from django.db import models
from api.cases.models import Cases  # Import model Cases dari file yang berbeda

class Documents(models.Model):
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
            ('closed', 'Closed'),
            ('on-progress', 'On Progress')
        ],
        default='open'  # Status default adalah 'open'
    )

    def __str__(self):
        return f"Update for {self.document.file_name} - {self.status}"