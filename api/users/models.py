from django.db import models

class Users(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('lawyer', 'Lawyer'),
    ]

    email = models.EmailField(unique=True)  # Email unik
    phone_number = models.CharField(max_length=15, unique=True)  # Nomor telepon unik
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)  # Peran user
    name = models.CharField(max_length=100)  # Nama user
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
    GENDER_CHOICES = [
        ('L', 'laki-laki'),
        ('P', 'perempuan'),
    ]

    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='lawyer')  # FK ke Users
    license_number = models.CharField(max_length=50, unique=True)  # Nomor lisensi unik
    specialization = models.CharField(max_length=100)  # Spesialisasi hukum
    experience_years = models.PositiveIntegerField()  # Tahun pengalaman
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)  # Jenis kelamin
    age = models.PositiveIntegerField()  # Usia
    availability = models.CharField(max_length=11, choices=AVAILABILITY_CHOICES, default='available')  # Status ketersediaan
    is_verified = models.BooleanField(default=False)  # Status verifikasi

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan
    updated_at = models.DateTimeField(auto_now=True)      # Waktu terakhir diperbarui

    def __str__(self):
        return f"{self.user.name} - {self.specialization}"


class Clients(models.Model):
    GENDER_CHOICES = [
        ('L', 'laki-laki'),
        ('P', 'perempuan'),
    ]

    user = models.OneToOneField('Users', on_delete=models.CASCADE, related_name='client')  # FK ke Users
    nik = models.CharField(max_length=16, unique=True)  # Nomor Identitas unik
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)  # Jenis kelamin
    age = models.PositiveIntegerField()  # Usia
    is_verified = models.BooleanField(default=False)  # Status verifikasi

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Waktu pembuatan
    updated_at = models.DateTimeField(auto_now=True)      # Waktu terakhir diperbarui

    def __str__(self):
        return f"{self.user.name} (NIK: {self.nik})"
