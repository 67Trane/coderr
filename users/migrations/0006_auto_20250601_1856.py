# users/migrations/0006_auto_create_guest_users.py

from django.db import migrations, IntegrityError, transaction
from django.contrib.auth.hashers import make_password


def create_guest_users(apps, schema_editor):
    User    = apps.get_model("users", "User")
    Profile = apps.get_model("users", "Profile")
    Token   = apps.get_model("authtoken", "Token")

    # 1) Gast-Business anlegen oder updaten
    guest_biz, _ = User.objects.update_or_create(
        username="kevin",
        defaults={
            "email": "guest_business@example.com",
            "type": "business",
            "password": make_password("asdasd24"),
            "is_active": True,
        }
    )
    # Token‐Erzeugung in einem separaten Savepoint:
    try:
        with transaction.atomic():
            Token.objects.create(user=guest_biz)
    except IntegrityError:
        # Falls zufällig genau derselbe Key generiert wurde, 
        # wird nur dieser Savepoint zurückgerollt, 
        # und die Migration insgesamt kann weitermachen.
        pass

    # Profil für Business-Gast (leg“e nur einmal” an)
    Profile.objects.get_or_create(user=guest_biz)


    # 2) Gast-Customer anlegen oder updaten
    guest_cust, _ = User.objects.update_or_create(
        username="andrey",
        defaults={
            "email": "guest_customer@example.com",
            "type": "customer",
            "password": make_password("asdasd"),
            "is_active": True,
        }
    )
    # Ebenfalls in einem eigenen Savepoint:
    try:
        with transaction.atomic():
            Token.objects.create(user=guest_cust)
    except IntegrityError:
        pass

    Profile.objects.get_or_create(user=guest_cust)


class Migration(migrations.Migration):

    dependencies = [
        ("users",    "0005_guestbusiness_guestcustomer"),
        ("authtoken","0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_guest_users),
    ]
