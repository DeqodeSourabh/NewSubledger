from django.contrib import admin

from .models import Profile, INRTransaction, CryptoTransaction, CryptoLedger

admin.site.register(Profile)
admin.site.register(INRTransaction)
admin.site.register(CryptoTransaction)
admin.site.register(CryptoLedger)


