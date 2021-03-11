from rest_framework import serializers
from . models import User, UserProfile, Auction, Bidding


class SignUpSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name", "avatar"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["present_address", "permanent_address", "avatar"]


class AuctionSerializer(serializers.ModelSerializer):
    files = serializers.ListField(
        child=serializers.FileField(allow_empty_file=False)
    )

    class Meta:
        model = Auction
        fields = ["auction_title", "auction_description", "base_price", "start_date", "end_date", "files"]


class BiddingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bidding
        fields = ["bid_amount"]
