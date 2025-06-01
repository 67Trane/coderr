from rest_framework import serializers
from users.models import User, Profile
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    user_id = serializers.IntegerField(source="id", read_only=True)
    date_joined = serializers.DateTimeField(source="user.date_joined", read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'type', 'user_id', 'date_joined',]


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_id = serializers.IntegerField(source="id", read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'type', 'user_id', 'password', 'token']

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()

        token, _ = Token.objects.get_or_create(user=user)
        user.token = token.key
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError(
                        "Benutzerkonto is deaktiviert.")
                token_obj, _ = Token.objects.get_or_create(user=user)
                data["token"] = token_obj.key
                return data
            else:
                raise serializers.ValidationError(
                    "Ungültiger Benutzername oder Passwort")
        else:
            raise serializers.ValidationError(
                "Beide Felder (username, password) sind erfolderlich.")
