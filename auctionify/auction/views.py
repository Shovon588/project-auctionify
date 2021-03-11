from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from rest_framework.permissions import IsAuthenticated
from . models import User, UserProfile, Auction, AuctionImage, Bidding

# Create your views here.


class SignUpView(APIView):
    serializer_class = serializers.SignUpSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get('password')
            user = serializer.save()
            user.set_password(password)
            user.is_active = True
            user.save()

            profile = UserProfile()
            profile.user = user
            profile.save()

            return Response({
                "status": "success",
                "message": "New user created successfully."
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({
                "status": "failed",
                "message": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)


class UpdateUserProfile(APIView):
    serializer_class = serializers.UserProfileSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get("avatar")
        return Response("Miao")


class CreateAuction(APIView):
    serializer_class = serializers.AuctionSerializer
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            auction_title = serializer.validated_data.get("auction_title")
            auction_description = serializer.validated_data.get("auction_description")
            base_price = serializer.validated_data.get("base_price")
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")

            auction = Auction.objects.create(user=request.user, auction_title=auction_title, auction_description=auction_description,
                              base_price=base_price, start_date=start_date, end_date=end_date)

            files = serializer.validated_data.get("files")
            for file in files:
                AuctionImage.objects.create(user=request.user, auction=auction, file=file)

            return Response({"status": "success", "message": "A new auction has been created.",
                             "data": {"title": auction_title, "description": auction_description,
                                      "base_price": base_price, "slug": auction.auction_slug}},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "failed", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class BiddingView(APIView):
    serializer_class = serializers.BiddingSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        serializer = self.serializer_class(data=request.data)
        try:
            auction = Auction.objects.get(auction_slug=slug)
        except Auction.DoesNotExist:
            return Response({"status": "error", "message": "Invalid auction slug."}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            bid_amount = serializer.validated_data.get("bid_amount")
            bid = Bidding.objects.create(user=request.user, auction=auction, bid_amount=bid_amount)

            return Response({'status': "success", "message": "New bid placed successfully.",
                             "data": {"auction": auction.auction_title, "bid_amount": bid.bid_amount, "bid_time": bid.bid_time}},
                            status=status.HTTP_201_CREATED)


        else:
            return Response({'status': "failed", "message": serializer.errors},
                            status=status.HTTP_400_BAD_REQUEST)
