from django.db import models
from api.users.models import Lawyers, Users, Clients
from api.common.utils import generate_unique_id
# Create your models here.
class Cases(models.Model):
    case_id = models.CharField(primary_key=True, default=generate_unique_id, editable=False, max_length=8, unique=True)
    client_id = models.ForeignKey(
        Clients,
        on_delete=models.CASCADE,
        related_name='cases'  # related_name untuk akses dari model Clients
    )
    lawyer_id = models.ForeignKey(
        Lawyers,
        on_delete=models.CASCADE,
        related_name='cases',
        null=True  # related_name untuk akses dari model Lawyers
    )
    user_id = models.ForeignKey(
        Users,
        on_delete=models.CASCADE,
        related_name='cases'  # related_name untuk akses dari model Users
    )
    Title = models.CharField(max_length=255)  # Informasi siapa yang membuat kasus
    case_type = models.CharField(max_length=255)  # Jenis kasus, tipe varchar dengan panjang 255 karakter
    created_by = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu saat kasus dibuat
    description = models.TextField()  # Deskripsi kasus
    status = models.CharField(
        max_length=20,
        choices=[
            ('approved', 'Approved'),
            ('reject', 'Reject')
        ],
        null=True  # Status dapat bernilai NULL
    )
    is_anonymous = models.BooleanField(default=False)  # Apakah kasus bersifat anonim

    def __str__(self):
        return f"Case: {self.case_type} - {self.status or 'No Status'}"