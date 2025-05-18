from rest_framework import serializers
from users.models import BusinessProfile

class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = '__all__'