# Generated by Django 5.1.2 on 2024-10-29 02:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0003_alter_message_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='file',
            field=models.FileField(blank=True, default=None, null=True, upload_to=''),
        ),
    ]
