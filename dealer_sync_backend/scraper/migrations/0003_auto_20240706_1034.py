# Generated by Django 3.2.25 on 2024-07-06 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0002_auto_20240706_0859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclelisting',
            name='image_url',
            field=models.URLField(max_length=500),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='msrp',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='vehiclelisting',
            name='title',
            field=models.CharField(max_length=500),
        ),
    ]
