# Generated by Django 4.2.16 on 2024-12-16 09:11

import api.common.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Conversations',
            fields=[
                ('conversation_id', api.common.fields.UniqueStringIDField(default=api.common.fields.UniqueStringIDField.generate_unique_id, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('message_id', api.common.fields.UniqueStringIDField(default=api.common.fields.UniqueStringIDField.generate_unique_id, editable=False, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('message_content', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.conversations')),
            ],
        ),
    ]
