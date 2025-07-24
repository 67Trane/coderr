from rest_framework import serializers
from orders_app.models import *


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value):
        try:
            return OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                "Offer detail with this ID does not exist."
            )

    def create(self, validated_data):
        offer_detaiL: OfferDetail = validated_data["offer_detail_id"]
        user = self.context["request"].user

        order = Order.objects.create(
            customer_user=user,
            business_user=offer_detaiL.offer.business_user,
            title=offer_detaiL.title,
            revisions=offer_detaiL.revisions,
            delivery_time_in_days=offer_detaiL.delivery_time_in_days,
            price=offer_detaiL.price,
            features=offer_detaiL.features,
            offer_type=offer_detaiL.offer_type,
            status="in_progress",
        )
        return order

    class Meta:
        model = Order
        fields = "__all__"
