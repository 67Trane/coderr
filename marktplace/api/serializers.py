from rest_framework import serializers
from marktplace.models import *


class OrderSerializer(serializers.ModelSerializer):
    offer_detail_id = serializers.IntegerField(write_only=True)

    def validate_offer_detail_id(self, value):
        try:
            return OfferDetail.objects.get(pk=value)
        except OfferDetail.DoesNotExist:
            raise serializers.ValidationError(
                "Offer detail with this ID does not exist.")

    def create(self, validated_data):
        offer_detaiL: OfferDetail = validated_data['offer_detail_id']
        user = self.context['request'].user

        order = Order.objects.create(
            customer_user=user,
            business_user=offer_detaiL.business_user,
            title=offer_detaiL.title,
            revisions=offer_detaiL.revisions,
            delivery_time_in_days=offer_detaiL.delivery_time_in_days,
            price=offer_detaiL.price,
            features=offer_detaiL.features,
            offer_type=offer_detaiL.offer_type,
            status="in_progress"
        )
        return order

    class Meta:
        model = Order
        fields = '__all__'


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='offerdetails-details',
        lookup_field='pk'
    )

    class Meta:
        model = OfferDetail
        fields = [
            'id',
            'url',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
            'business_user',
        ]


class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True)
    user = serializers.IntegerField(source='business_user.id', read_only=True)
    customer_user = serializers.PrimaryKeyRelatedField(read_only=True)
    business_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Offer
        fields = [
            "id",
            "user",
            "title", "description",
            "created_at", "updated_at",
            "image", "customer_user", "business_user", "details",
        ]

    def create(self, validated_data):
        details_data = validated_data.pop('details', [])
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop('details', None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail in details_data:
                OfferDetail.objects.create(offer=instance, **detail)

        return instance
