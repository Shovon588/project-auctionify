from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from . managers import UserManager
from autoslug import AutoSlugField


# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email Address")
    first_name = models.CharField(max_length=100, verbose_name="First Name", blank=True, null=True)
    last_name = models.CharField(max_length=100, verbose_name="Last Name", blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        # send_mail(subject, message, from_email, [self.email], **kwargs)    def get_full_name(self):

        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.email


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    present_address = models.CharField(max_length=512, blank=True, null=True)
    permanent_address = models.CharField(max_length=512, blank=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return self.user.email


class Auction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_title = models.CharField(max_length=512)
    auction_slug = AutoSlugField(populate_from="auction_title", unique=True, blank=True, null=True)
    auction_description = models.TextField()
    base_price = models.FloatField()

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.auction_slug


class AuctionImage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    file = models.FileField(upload_to="auction_files/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        file_name = self.file.name.split("/")[1]
        return "%s from %s, auction ID: %s" % (file_name, self.auction.auction_slug, self.auction.id)


class Bidding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    bid_amount = models.FloatField()

    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s bids %.2f for %s" %(self.user.email, self.bid_amount, self.auction.auction_title)
