# Generated by Django 5.2.1 on 2025-06-11 10:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("marktplace", "0006_offerdetail"),
    ]

    operations = [
        migrations.AddField(
            model_name="offer",
            name="revisions",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
