# Generated by Django 5.1.6 on 2025-02-15 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messages_logger', '0004_message_camera_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='alert_in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
