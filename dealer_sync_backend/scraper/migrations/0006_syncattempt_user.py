# Generated by Django 3.2.25 on 2024-07-07 05:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scraper', '0005_vehiclelisting_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='syncattempt',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sync_attempts', to=settings.AUTH_USER_MODEL),
        ),
    ]