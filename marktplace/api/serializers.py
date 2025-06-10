from rest_framework import serializers
from marktplace.models import *


class OrderSerializer(serializers.ModelSerializer):
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
            'url',
            'id',
            'title',
            'revisions',
            'delivery_time_in_days',
            'price',
            'features',
            'offer_type',
        ]


class OfferSerializer(serializers.ModelSerializer):
    details = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='offerdetails-details',
        lookup_field='pk'
    )

    class Meta:
        model = Offer
        fields = [
            "id",
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


        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail in details_data:
                OfferDetail.objects.create(offer=instance, **detail)

        return instance
