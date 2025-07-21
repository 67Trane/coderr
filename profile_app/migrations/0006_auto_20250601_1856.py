from django.db import migrations, transaction, IntegrityError
from django.contrib.auth.hashers import make_password
import secrets


def create_guest_users(apps, schema_editor):
    User = apps.get_model("users", "User")
    Profile = apps.get_model("users", "Profile")
    Token = apps.get_model("authtoken", "Token")

    # Gast-Accounts definieren
    guests = [
        {
            "username": "kevin",
            "email": "guest_business@example.com",
            "type": "business",
            "password": "asdasd24",
        },
        {
            "username": "andrey",
            "email": "guest_customer@example.com",
            "type": "customer",
            "password": "asdasd",
        },
    ]

    for info in guests:
        # User anlegen oder updaten
        guest, _ = User.objects.update_or_create(
            username=info["username"],
            defaults={
                "email": info["email"],
                "type": info["type"],
                "password": make_password(info["password"]),
                "is_active": True,
            },
        )
        # Token nur anlegen, wenn noch keiner existiert
        if not Token.objects.filter(user=guest).exists():
            # Manuelle Key-Generierung mit Kollision-Abfang
            for _ in range(5):
                key = secrets.token_hex(20)
                try:
                    with transaction.atomic():
                        Token.objects.create(user=guest, key=key)
                    break
                except IntegrityError:
                    # bei Kollision: nächsten Versuch
                    continue
        # Profil sicherstellen
        Profile.objects.get_or_create(user=guest)


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0005_guestbusiness_guestcustomer"),
        ("authtoken", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_guest_users),
    ]
