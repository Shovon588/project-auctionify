from django.contrib import admin
from . models import User, UserProfile, Auction, AuctionImage, Bidding

# Register your models here.
admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(Auction)
admin.site.register(AuctionImage)
admin.site.register(Bidding)
