# Generated by Django 4.2.16 on 2024-12-16 09:11

import api.common.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cases',
            fields=[
                ('case_id', api.common.fields.UniqueStringIDField(default=api.common.fields.UniqueStringIDField.generate_unique_id, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('case_type', models.CharField(max_length=255)),
                ('created_by', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField()),
                ('status', models.CharField(choices=[('approved', 'Approved'), ('reject', 'Reject')], max_length=20, null=True)),
                ('is_anonymous', models.BooleanField(default=False)),
            ],
        ),
    ]
