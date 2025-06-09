from rest_framework import serializers
from marktplace.models import *



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OfferDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfferDetail
        fields = '__all__'
        

class OfferSerializer(serializers.ModelSerializer):
    details = OfferDetailSerializer(many=True, read_only=True)
    user = serializers.IntegerField(source='business_user_id', read_only=True)
    class Meta:
        model = Offer
        fields = [
            "id", "user",
            "title", "description",
            "created_at", "updated_at",
            "image", "customer_user", "business_user", "details",
        ]


