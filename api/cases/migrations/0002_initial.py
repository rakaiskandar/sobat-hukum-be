# Generated by Django 4.2.16 on 2024-12-04 08:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('cases', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='cases',
            name='client_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='users.clients'),
        ),
        migrations.AddField(
            model_name='cases',
            name='lawyer_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='users.lawyers'),
        ),
        migrations.AddField(
            model_name='cases',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to=settings.AUTH_USER_MODEL),
        ),
    ]
