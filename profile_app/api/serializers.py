from rest_framework import serializers
from profile_app.models import  Profile

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email")
    type = serializers.CharField(source="user.type", read_only=True)
    first_name = serializers.CharField(source="user.first_name", required=False)
    last_name = serializers.CharField(source="user.last_name", required=False)
    created_at = serializers.DateTimeField(source="user.date_joined", read_only=True)

    file = serializers.ImageField(required=False, allow_null=True)
    location = serializers.CharField(required=False, allow_null=True)
    tel = serializers.CharField(required=False, allow_null=True)
    description = serializers.CharField(required=False, allow_null=True)
    working_hours = serializers.CharField(required=False)
    class Meta:
        model = Profile
        fields = [
            "user",
            "username",
            "first_name",
            "last_name",
            "file",
            "location",
            "tel",
            "description",
            "working_hours",
            "type",
            "email",
            "created_at",
        ]

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", {})

        if user_data:
            user = instance.user

            first_name = user_data.get("first_name", None)
            last_name = user_data.get("last_name", None)
            email = user_data.get("email", None)

            if first_name is not None:
                user.first_name = first_name
            if last_name is not None:
                user.last_name = last_name
            if email is not None:
                user.email = email

            user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


