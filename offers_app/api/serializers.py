from rest_framework import serializers
from offers_app.models import Offer, OfferDetail
from authentication_app.models import User

"""
Serializers for the offers_app, handling representation and validation of Offer and OfferDetail models.

Classes:
    UserDetailsSerializer: Nested serializer for business user basic info.
    OfferDetailSerializer: Provides hyperlink to individual OfferDetail instances.
    OfferSingleDetailSerializer: Detailed representation for creating/updating OfferDetail entries.
    OfferSerializer: Main serializer for Offer model, including nested details, price and delivery summaries.
"""


class UserDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for business user basic information nested in Offer responses.

    Fields:
        first_name (str): User's first name.
        last_name (str): User's last name.
        username (str): User's username.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferDetailSerializer(serializers.ModelSerializer):
    """
    Hyperlinked serializer for OfferDetail instances.

    Adds:
        url (HyperlinkedIdentityField): Link to the detail view for this OfferDetail.
    """

    url = serializers.HyperlinkedIdentityField(
        view_name="offerdetails-details", lookup_field="pk"
    )

    class Meta:
        model = OfferDetail
        fields = ["id", "url"]


class OfferSingleDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for nested creation/update of individual OfferDetail entries.

    Validates presence of offer_type and exposes all relevant fields.

    Fields:
        id (int): Detail primary key (read-only on update).
        title (str): Title of this detail.
        revisions (int): Number of allowed revisions.
        delivery_time_in_days (int): Estimated delivery time.
        price (decimal): Price for this detail.
        features (list): List of feature descriptions.
        offer_type (str): Required type identifier for the detail.
    """

    offer_type = serializers.CharField(required=True)

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "title",
            "revisions",
            "delivery_time_in_days",
            "price",
            "features",
            "offer_type",
        ]


class OfferSerializer(serializers.ModelSerializer):
    """
    Main serializer for Offer model with nested details and summary fields.

    - Allows creation and update of nested OfferDetail objects.
    - Computes min_price and min_delivery_time across details.
    - Exposes business_user id and nested user_details for convenience.
    """

    details = OfferSingleDetailSerializer(many=True)
    user = serializers.IntegerField(source="business_user.id", read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)
    user_details = UserDetailsSerializer(source="business_user", read_only=True)
    min_price = serializers.IntegerField(read_only=True)
    min_delivery_time = serializers.IntegerField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title",
            "description",
            "created_at",
            "updated_at",
            "image",
            "business_user",
            "details",
            "min_price",
            "min_delivery_time",
            "user_details",
        ]

    def create(self, validated_data):
        """
        Create an Offer instance and nested OfferDetail objects from validated data.

        Args:
            validated_data (dict): Contains 'details' list and other Offer fields.

        Returns:
            Offer: Newly created Offer with associated details.
        """
        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        """
        Update an Offer instance and replace nested OfferDetail objects if provided.

        Args:
            instance (Offer): The existing Offer instance.
            validated_data (dict): May include 'details' and other Offer fields.

        Returns:
            Offer: Updated Offer instance.
        """
        details_data = validated_data.pop("details", None)

        # Update Offer fields
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        # If details provided, replace existing relations
        if details_data is not None:
            instance.details.all().delete()
            for detail in details_data:
                OfferDetail.objects.create(offer=instance, **detail)

        return instance

    def validate_details(self, value):
        """
        Ensure each detail dict contains the required 'offer_type' field.

        Args:
            value (list): List of detail dicts.

        Raises:
            serializers.ValidationError: If any detail missing 'offer_type'.

        Returns:
            list: The validated list if all entries are valid.
        """
        for idx, detail in enumerate(value):
            if not detail.get("offer_type"):
                raise serializers.ValidationError(
                    {idx: "This detail is missing the required field 'offer_type'."}
                )
        return value
