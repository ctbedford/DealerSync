# Generated by Django 3.2.25 on 2024-07-20 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('scraper', '0008_auto_20240711_0434'),
    ]

    operations = [
        migrations.AddField(
            model_name='syncattempt',
            name='task_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='syncattempt',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='sync_attempts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_listings', to=settings.AUTH_USER_MODEL),
        ),
    ]
