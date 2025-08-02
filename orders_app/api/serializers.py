from rest_framework import serializers
from orders_app.models import Order, OfferDetail

"""
Serializers for the orders_app, managing creation and validation of Order instances.

Classes:
    OrderSerializer: Handles validating an OfferDetail ID and creating an Order for the current user.
"""


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model that facilitates ordering a specific OfferDetail.

    Fields:
        offer_detail_id (int): ID of the OfferDetail to order (write-only).
        All other Order model fields (read/write as defined in Meta).

    Methods:
        validate_offer_detail_id: Ensures the provided OfferDetail exists.
        create: Creates an Order linking customer, business, and detail properties.
    """

    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value):
        """
        Validate that an OfferDetail with the given primary key exists.

        Args:
            value (int): OfferDetail primary key provided by the client.

        Raises:
            serializers.ValidationError: If no OfferDetail matches the given ID.

        Returns:
            OfferDetail: The retrieved OfferDetail instance.
        """
        try:
            return OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                "Offer detail with this ID does not exist."
            )

    def create(self, validated_data):
        """
        Build and save a new Order using the validated OfferDetail and current user.

        - Extracts the OfferDetail instance from validated_data.
        - Determines customer and business users from context and detail.
        - Copies title, revisions, delivery_time, price, features, and type from detail.
        - Sets initial status to 'in_progress'.

        Args:
            validated_data (dict): Includes 'offer_detail_id' and other Order defaults.

        Returns:
            Order: Newly created Order instance.
        """
        offer_detail: OfferDetail = validated_data["offer_detail_id"]
        user = self.context["request"].user

        order = Order.objects.create(
            customer_user=user,
            business_user=offer_detail.offer.business_user,
            title=offer_detail.title,
            revisions=offer_detail.revisions,
            delivery_time_in_days=offer_detail.delivery_time_in_days,
            price=offer_detail.price,
            features=offer_detail.features,
            offer_type=offer_detail.offer_type,
            status="in_progress",
        )
        return order

    class Meta:
        """
        Meta settings for OrderSerializer.

        - model: Order
        - fields: Include all model fields, with 'offer_detail_id' write-only.
        """

        model = Order
        fields = "__all__"
