from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=64, blank=True, null=True)
    last_name = models.CharField(max_length=64, blank=True, null=True)
    address = models.CharField(max_length=64, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='profile_pic', blank=True, null=True)

    def __str__(self):
        return self.user.username


class AuctionItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=128)
    item_description = models.CharField(max_length=1024)
    item_cover_phone = models.ImageField(upload_to="item_main_image", default="item_main_image/fb.png")
    base_price = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return self.item_name


class AuctionItemImage(models.Model):
    item = models.ForeignKey(AuctionItem, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="item_images")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.item.item_name
