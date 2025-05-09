# Generated by Django 5.2 on 2025-04-30 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_user_nickname"),
    ]

    operations = [
        migrations.CreateModel(
            name="OTP",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("phone_number", models.CharField(max_length=15)),
                ("code", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_verified", models.BooleanField(default=False)),
            ],
            options={
                "verbose_name": "OTP",
                "verbose_name_plural": "OTPs",
            },
        ),
    ]
