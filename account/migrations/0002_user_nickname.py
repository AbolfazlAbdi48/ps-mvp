# Generated by Django 5.2 on 2025-04-22 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="nickname",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                unique=True,
                verbose_name="Nick Name",
            ),
        ),
    ]
