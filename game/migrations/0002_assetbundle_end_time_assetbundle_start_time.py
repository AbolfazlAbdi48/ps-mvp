# Generated by Django 5.2 on 2025-04-23 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="assetbundle",
            name="end_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="End"),
        ),
        migrations.AddField(
            model_name="assetbundle",
            name="start_time",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Start"),
        ),
    ]
