# Generated by Django 5.2.1 on 2025-06-08 14:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marktplace", "0004_alter_offer_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="offer",
            name="user",
        ),
        migrations.AddField(
            model_name="offer",
            name="business_user",
            field=models.ForeignKey(
                limit_choices_to={"type": "business"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offer_as_business",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="offer",
            name="customer_user",
            field=models.ForeignKey(
                limit_choices_to={"type": "customer"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="offer_as_customer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
