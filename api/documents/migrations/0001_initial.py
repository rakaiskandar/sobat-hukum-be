# Generated by Django 4.2.16 on 2024-11-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=255)),
                ('file_path', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('case_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='document', to='cases.cases')),
            ],
        ),
        migrations.CreateModel(
            name='CasesUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_detail', models.TextField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('closed', 'Closed'), ('on-progress', 'On Progress')], default='open', max_length=20)),
                ('document_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='updates', to='documents.documents')),
            ],
        ),
    ]
