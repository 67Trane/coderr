from rest_framework import serializers
from users.models import User, Profile
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    type = serializers.CharField(source="user.type", read_only=True)
    user_id = serializers.IntegerField(source="id", read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'type', 'user_id']


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
