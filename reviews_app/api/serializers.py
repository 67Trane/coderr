from rest_framework import serializers
from reviews_app.models import Review
from authentication_app.models import User

"""
Serializer for the reviews_app, handling validation and creation of Review instances.

Classes:
    ReviewSerializer: Validates rating, business_user, and description fields for submissions.
"""


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model with custom validation messages.

    Fields:
        business_user (PrimaryKeyRelatedField): Must reference a valid business user.
        reviewer (HiddenField): Automatically set from request context (not exposed).
        rating (IntegerField): Required rating between 1 and above, with custom error messages.
        description (CharField): Required non-empty review text.

    Meta:
        model: Review
        fields: All fields on the model.
    """

    business_user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type="business"),
        required=True,
        help_text="ID of the business user being reviewed",
    )
    rating = serializers.IntegerField(
        min_value=1,
        required=True,
        error_messages={
            "min_value": "Rating muss mindestens 1 sein.",
            "invalid": "Rating muss eine ganze Zahl sein.",
        },
        help_text="Numeric rating for the review, minimum 1",
    )
    description = serializers.CharField(
        required=True,
        help_text="Text description for the review",
    )

    class Meta:
        model = Review
        fields = "__all__"

    def create(self, validated_data):
        """
        Override creation to automatically assign the requesting customer as the reviewer.

        Args:
            validated_data (dict): Validated input data, including business_user, rating, description.

        Returns:
            Review: Newly created Review instance.
        """
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["reviewer"] = request.user
        return super().create(validated_data)
