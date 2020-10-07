from django.contrib import admin

from . models import UserProfile, AuctionItem, AuctionItemImage

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(AuctionItem)
admin.site.register(AuctionItemImage)

