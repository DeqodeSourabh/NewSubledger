from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

User = settings.AUTH_USER_MODEL

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    profile_photo = models.ImageField(default="default.png", upload_to='profile_photos')

def user_did_save(sender, instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

post_save.connect(user_did_save, sender=User)

class INRTransaction(models.Model):
    user = models.CharField(max_length=10)
    balance = models.FloatField(default=0.0)
    deposit = models.FloatField(default=0.0)
    withdraw = models.FloatField(default=0.0)

class CryptoTransaction(models.Model):
    asset = models.IntegerField(max_length=10)
    balance = models.FloatField(default=0.0)
    deposit = models.FloatField(default=0.0)
    withdraw = models.FloatField(default=0.0)

class CryptoLedger(models.Model):
    fromAdd = models.CharField(max_length=10, default="hi")
    toAdd = models.CharField(max_length = 10, default="hi")
    tokenId = models.IntegerField()
    quantity = models.FloatField()
