# Generated by Django 5.1.2 on 2024-11-23 15:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0021_alter_privatechatroom_creator'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='publicchatroom',
            name='users_online',
            field=models.ManyToManyField(blank=True, related_name='online_in_public_groups', to=settings.AUTH_USER_MODEL),
        ),
    ]
