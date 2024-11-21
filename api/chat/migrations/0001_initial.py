# Generated by Django 4.2.16 on 2024-11-20 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('cases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('case_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_case', to='cases.cases')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_client', to='users.clients')),
                ('lawyer_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conversations_lawyer', to='users.lawyers')),
            ],
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_content', models.TextField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('is_read', models.BooleanField(default=False)),
                ('conversation_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.conversations')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='users.users')),
            ],
        ),
    ]