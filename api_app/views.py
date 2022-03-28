import io
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rest_framework import viewsets
from .models import CryptoTransaction, Profile, INRTransaction, CryptoLedger
from .serializers import ShowCryptoSerializer, walletSerializer, transactionSerializer, amountSerializer, withdrawSerializer, cryptoSerailizers, CryptoLedgerSerializer
from django.db import transaction
from django.db.models import F
#from rest_framework.parsers import JSONParser

class TransactionViewSet(viewsets.ModelViewSet):
    model = INRTransaction
    queryset = INRTransaction.objects.all()
    print(queryset)
    for  i in queryset:
        serializer_class = transactionSerializer(data={"user":i.user,"balance":i.balance,"deposit":i.deposit,"withdraw":i.withdraw})

class CryptoTransactionViewSet(viewsets.ModelViewSet):
    model = CryptoTransaction
    queryset = CryptoTransaction.objects.all()
    serializer_class = cryptoSerailizers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_balance_view(request, *args, **kwargs):
    try:
        qs = User.objects.filter(username=request.user)[0].profile
        serializer = walletSerializer(qs)
        print(type(serializer))
        balance = serializer.data['balance']
        print(serializer.data['balance'])
        return Response(serializer.data, status=200)
    except:
        return Response({"Something went wrong. Please try again later."}, status=404)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit_balance_view(request, *args, **kwargs):
    try:
        with transaction.atomic():
            amount_to_deposit = float(request.data.get("amount"))
            serializer= amountSerializer(data=request.data)

            if serializer.is_valid(raise_exception=True):
                qs = User.objects.select_for_update().filter(username=request.user)[0].profile
                qs.balance = qs.balance + amount_to_deposit
                qs.save()
                transaction1 = INRTransaction(user = request.user, deposit = amount_to_deposit, balance = qs.balance)
                transaction1.save()
                return Response({"Deposit successful."}, status=200)
    except Exception as e:
        return Response({"Something went wrong. Please try again later."}, status=404)




@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw_balance_view(request, *args, **kwargs):
    try:
        qs = User.objects.select_for_update().filter(username=request.user)[0].profile
        serializer= withdrawSerializer(data={"amount":float(request.data.get("amount")), "balance": qs.balance})
        if serializer.is_valid(raise_exception=True):
            amount_to_withdraw = float(request.data.get("amount"))
            qs.balance = qs.balance - amount_to_withdraw
            qs.save()
            return Response({"Withdraw successful."}, status=200)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=404)

#  ------------------------------------Crypto Convert-----------------------------------------------


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def crypto_deposit_balance_view(request, *args, **kwargs):
    try:
        with transaction.atomic():
            fromAdd = request.data.get("fromAdd")
            toAdd = request.data.get("toAdd")
            tokenId = request.data.get("tokenId")
            quantity = request.data.get("quantity")
            print(tokenId, quantity, fromAdd, toAdd)
            serializer= CryptoLedgerSerializer(data={"tokenId":tokenId, "quantity": quantity}) 
            if serializer.is_valid(raise_exception=True):
                crypto = CryptoLedger(tokenId= tokenId, fromAdd= fromAdd, toAdd=toAdd , quantity= quantity)
                crypto.save()
            return Response({"Deposit successful."}, status=200)
    except Exception as e:
        print(e)
        return Response({"Something went wrong. Please try again later."}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def show_crypto_balance_view(request, *args, **kwargs):
    try:        
        qs = CryptoLedger.objects.all()
        print(qs[0].quantity, qs[0].tokenId)
        
        for i in qs: 
            print('helllp')
            serializer = ShowCryptoSerializer(i)
            tokenId = serializer.data['tokenId']
            quantity = serializer.data['quantity']
            print(tokenId, quantity)
            return Response(serializer.data, status=200)
    except:
        return Response({"Something went wrong. Please try again later."}, status=404)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def Crypto_withdraw_balance_view(request, *args, **kwargs):
#     try:
#         with transaction.atomic():
#             tokenId = request.data.get('tokenId')
#             quantity = request.data.get("quantity")
#             serializer= CryptoLedgerSerializer(data= {"tokenId":tokenId, "quantity": quantity})
            
            
#             if serializer.is_valid(raise_exception=True):
#                # qs = CryptoLedger.objects.select_for_update().get(tokenID = tokenId)
#                #type = "withdraw"
#                 qs.save()

#                 transaction1 = CryptoLedger(user = request.user, quantity = quantity, balance = qs.balance,txn_type= type )
#                 transaction1.save()
            
            
#                 return Response({"Deposit successful."}, status=200)
#     except Exception as e:
#         print(e)
#         return Response({"Something went wrong. Please try again later."}, status=404)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def crypto_convert(request,  *args, **kwargs):
#     with transaction.atomic():
#         amount = request.data.get("amount")
#         # fromAsset = request.data.get("from")
#         # toAsset = request.data.get("to")
#         # print(fromAsset, toAsset)
#         qs1 = CryptoTransaction.objects.select_for_update().get(asset = 1)
#         print(qs1.deposit)
#         print(qs1.balance)
        
        
#         from_price1 = 10.0
#         to_price1 = 1000
#         net_price = from_price1/to_price1

#         qs1.balance = qs1.balance - from_price1
#         qs1.withdraw = from_price1
#         qs1.save()

#         qs2 = CryptoTransaction.objects.select_for_update().get(asset = 2)
#         qs2.balance = qs2.balance + from_price1
#         qs2.deposit = from_price1

#         qs2.save()

#         return Response({"Withdraw successful."}, status=200)

