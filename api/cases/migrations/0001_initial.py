# Generated by Django 4.2.16 on 2024-11-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_type', models.CharField(max_length=255)),
                ('created_by', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('reject', 'Reject')], max_length=20, null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='users.clients')),
                ('lawyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='users.lawyers')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='users.users')),
            ],
        ),
    ]
