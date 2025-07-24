from rest_framework import serializers
from offers_app.models import *
from authentication_app.models import User


class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username"]


class OfferDetailSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="offerdetails-details", lookup_field="pk"
    )

    class Meta:
        model = OfferDetail
        fields = [
            "id",
            "url",
        ]


class OfferSingleDetailSerializer(serializers.ModelSerializer):
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

        details_data = validated_data.pop("details", [])
        offer = Offer.objects.create(**validated_data)
        for detail in details_data:
            OfferDetail.objects.create(offer=offer, **detail)
        return offer

    def update(self, instance, validated_data):
        details_data = validated_data.pop("details", None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if details_data is not None:
            instance.details.all().delete()
            for detail in details_data:
                OfferDetail.objects.create(offer=instance, **detail)

        return instance
