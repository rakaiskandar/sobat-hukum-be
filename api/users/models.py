from django.db import models
from django.contrib.auth.models import AbstractUser
from api.common.fields import UniqueStringIDField

class Users(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('lawyer', 'Lawyer'),
    ]
    GENDER_CHOICES = [
        ('L', 'laki-laki'),
        ('P', 'perempuan'),
    ]
    user_id = UniqueStringIDField(primary_key=True)
    email = models.EmailField(unique=True)  # Email unik
    phone_number = models.CharField(max_length=15, unique=True)  # Nomor telepon unik
    role = models.CharField(max_length=10, choices=ROLE_CHOICES) 
    username = models.CharField(max_length=100, unique=True, default="default_username") # Peran user
    name = models.CharField(max_length=100)  # Nama user
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True)  # Jenis kelamin
    age = models.PositiveIntegerField(null=True)  # Usia
    password = models.CharField(max_length=128)  # Password (hashed)
    profile_picture = models.CharField(max_length=128, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan
    updated_at = models.DateTimeField(auto_now=True)      # Waktu terakhir diperbarui

    def __str__(self):
        return f"{self.name} ({self.role})"


class Lawyers(models.Model):
    AVAILABILITY_CHOICES = [
        ('available', 'Available'),
        ('unavailable', 'Unavailable'),
    ]
    lawyer_id = UniqueStringIDField(primary_key=True)
    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='lawyer')  # FK ke Users
    license_number = models.CharField(max_length=50, null=True, unique=True)  # Nomor lisensi unik
    specialization = models.CharField(max_length=100, null=True)  # Spesialisasi hukum
    experience_years = models.PositiveIntegerField(null=True)  # Tahun pengalaman
    availability = models.CharField(max_length=11, choices=AVAILABILITY_CHOICES, default='available')  # Status ketersediaan
    is_verified = models.BooleanField(default=False)  # Status verifikasi

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan
    updated_at = models.DateTimeField(auto_now=True)      # Waktu terakhir diperbarui

    def __str__(self):
        return f"{self.user.name} - {self.specialization}"


class Clients(models.Model):
    client_id = UniqueStringIDField(primary_key=True)
    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='client')  # FK ke Users
    nik = models.CharField(max_length=16, unique=True, null=True)  # Nomor Identitas unik
    is_verified = models.BooleanField(default=False)  # Status verifikasi

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan
    updated_at = models.DateTimeField(auto_now=True)      # Waktu terakhir diperbarui

    def __str__(self):
        return f"{self.user.name} (NIK: {self.nik})"
