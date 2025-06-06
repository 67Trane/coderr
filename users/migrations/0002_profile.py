# Generated by Django 5.2.1 on 2025-05-31 18:54

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Profile",
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
                ("username", models.CharField(max_length=200)),
                ("email", models.CharField(max_length=200)),
                (
                    "type",
                    models.CharField(
                        choices=[("business", "Business"), ("customer", "Customer")],
                        default="customer",
                        max_length=20,
                    ),
                ),
            ],
        ),
    ]
