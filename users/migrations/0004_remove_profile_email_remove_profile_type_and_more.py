# Generated by Django 5.2.1 on 2025-05-31 21:54

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0003_profile_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="profile",
            name="email",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="type",
        ),
        migrations.RemoveField(
            model_name="profile",
            name="username",
        ),
    ]
