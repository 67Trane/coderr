# Generated by Django 5.2.1 on 2025-06-08 16:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marktplace", "0005_remove_offer_user_offer_business_user_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="OfferDetail",
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
                ("delivery_time_in_days", models.IntegerField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("features", models.JSONField(blank=True, default=list)),
                (
                    "offer_type",
                    models.CharField(
                        choices=[
                            ("basic", "Basic"),
                            ("standard", "Standard"),
                            ("premium", "Premium"),
                        ],
                        max_length=10,
                    ),
                ),
                (
                    "offer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="details",
                        to="marktplace.offer",
                    ),
                ),
            ],
        ),
    ]
