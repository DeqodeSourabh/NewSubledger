from tokenize import String
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CryptoTransaction, Profile, INRTransaction, CryptoLedger, user_did_save

class walletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        #balance should be integer and positive
        balance = serializers.FloatField()

        def validate(self,data):
            balance = data.get('balance')
            if balance < 0.0 :
                raise serializers.ValidationError('amount cannot be negative')

        fields = ['balance', ]

class transactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = INRTransaction
        #validation for each fields
        def validate(self,data):
            #user 
            if data['user'] is not None or String:
                raise serializers.ValidationError('Not valid User')

            #balance
            if data['balance'] is not None or int:
                raise serializers.ValidationError('Not valid balance')
            #deposit
            if data['deposit'] is not None or int:
                raise serializers.ValidationError('Not valid deposit')
            #withdraw
            if data['withdraw'] is not None or int:
                raise serializers.ValidationError('Not valid withdraw')
        fields = ['user','balance','deposit','withdraw']
    
class amountSerializer(serializers.Serializer):
    amount = serializers.FloatField()

    def validate(self,data):
        
        if data['amount'] <0.0 :
            print(data['amount'])
            raise serializers.ValidationError('amount cannot be none or negative')
        
        if data['amount'] is  None:
            raise serializers.ValidationError('Amount and target can not be specified together')
        return data['amount']


class withdrawSerializer(serializers.Serializer):
    amount = serializers.FloatField()
    balance = serializers.FloatField()

    def validate(self,data):
        balance = data.get('balance')
        amount= data.get("amount")

        if amount <0.0 :
            raise serializers.ValidationError('amount cannot be none or negative')
        elif amount is  None:
            raise serializers.ValidationError('Amount and target can not be specified together')
        elif amount >balance:
            raise serializers.ValidationError('amount is greater then balance ')
        return amount


class cryptoSerailizers(serializers.Serializer):
    class Meta:
        model = CryptoTransaction
        fields = ['asset','balance', 'deposit', 'withdraw']

class CryptoLedgerSerializer(serializers.Serializer):
    tokenId = serializers.IntegerField()
    quantity = serializers.FloatField()

    def validate(self, data):
        quantity = data.get('quantity')
        tokenId1= data.get("tokenId")
        print(tokenId1, quantity)
        if tokenId1 is None or quantity is None :
            raise serializers.ValidationError("tokenId or quantity should not be empty")
        elif tokenId1 < 0 or quantity < 0:
            raise serializers.ValidationError("tokenId or quantity should not be empty")
        return quantity, tokenId1

class ShowCryptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoLedger
        fields = ['fromAdd','toAdd','tokenId','quantity']
        