# Generated by Django 4.2.16 on 2024-11-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('client', 'Client'), ('lawyer', 'Lawyer')], max_length=10)),
                ('name', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=128)),
                ('profile_picture', models.CharField(max_length=128, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Lawyers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('license_number', models.CharField(max_length=50, unique=True)),
                ('specialization', models.CharField(max_length=100)),
                ('experience_years', models.PositiveIntegerField()),
                ('gender', models.CharField(choices=[('L', 'laki-laki'), ('P', 'perempuan')], max_length=6)),
                ('age', models.PositiveIntegerField()),
                ('availability', models.CharField(choices=[('available', 'Available'), ('unavailable', 'Unavailable')], default='available', max_length=11)),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='lawyer', to='users.users')),
            ],
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nik', models.CharField(max_length=16, unique=True)),
                ('gender', models.CharField(choices=[('L', 'laki-laki'), ('P', 'perempuan')], max_length=6)),
                ('age', models.PositiveIntegerField()),
                ('is_verified', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='client', to='users.users')),
            ],
        ),
    ]
