from rest_framework import status
from orders_app.models import *
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews_app.models import Review
from profile_app.models import Profile
from offers_app.models import Offer


class BaseInfos(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        review_count = Review.objects.count()
        avg = (
            Review.objects.aggregate(average_rating=models.Avg("rating"))[
                "average_rating"
            ]
            or 0
        )
        business_profile_count = Profile.objects.filter(user__type="business").count()
        offer_count = Offer.objects.count()

        data = {
            "review_count": review_count,
            "average_rating": avg,
            "business_profile_count": business_profile_count,
            "offer_count": offer_count,
        }
        return Response(data, status=status.HTTP_200_OK)
