# Generated by Django 5.2.1 on 2025-07-24 10:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("offers_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("revisions", models.PositiveIntegerField(default=0)),
                ("delivery_time_in_days", models.IntegerField(blank=True, null=True)),
                (
                    "price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("features", models.JSONField(blank=True, default=list)),
                ("offer_type", models.CharField(blank=True, max_length=10, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True, null=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("in_progress", "In Progress"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                        ],
                        default="in_progress",
                        max_length=100,
                    ),
                ),
                (
                    "business_user",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"type": "business"},
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders_as_business",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "customer_user",
                    models.ForeignKey(
                        blank=True,
                        limit_choices_to={"type": "customer"},
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders_as_customer",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "offer_detail",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="offer_details",
                        to="offers_app.offerdetail",
                    ),
                ),
            ],
        ),
    ]
