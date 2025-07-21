from rest_framework import serializers
from reviews_app.models import Review
from profile_app.models import User


class ReviewSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)
    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type="business"),
        required=True
    )

    rating = serializers.IntegerField(min_value=1, error_messages={
                                      "min_value": "Rating muss mindestens 1 sein.", "invalid": "Rating muss eine ganze Zahl sein."}, required=True)

    class Meta:
        model = Review
        fields = "__all__"
