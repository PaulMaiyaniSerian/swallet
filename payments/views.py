from django.shortcuts import render
import decimal

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# mpesa utils
from .mpesa import utils, helpers

# models import
from .models import C2BMpesaTransaction, LNMTransaction, JointLmnC2BTransaction
from accounts.models import UserWallet

# serializers
from .serializers import C2BMpesaTransactionSerializer, JointLmnC2BTransactionSerializer

class RegisterMpesaCallBackUrlsView(generics.GenericAPIView):

    def post(self, request):
        result = utils.register_callbackurls()

        if result.get("ResponseCode") == "0":
            return Response(data=result, status=status.HTTP_200_OK)
        elif result.get("ResponseCode") == "500":
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class C2BValidationView(generics.GenericAPIView):
    # return no message since saf is not returning a response to the validation url
    def post(self, request):
        print(request.data, "validations")

        return Response(status=status.HTTP_200_OK)
    



class SimulateC2BTransactionView(generics.GenericAPIView):

    def post(self, request):
        # print(request.data)
        account_number = request.data.get("account_number")
        amount = request.data.get("amount")

        if account_number and amount:
            result = utils.simulate_c2b_transaction(account_number, amount)
            if result.get("ResponseCode") == "0":
                return Response(data=result, status=status.HTTP_200_OK)
            elif result.get("ResponseCode") == "500":
                return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            message = {
                "error": "please provide the account number and amount"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

class StkPushProcessApiView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]
    def post(self, request):
        # print(request.data)
        account_number = None
        # get logged in user account number
        try:
            account_number = UserWallet.objects.get(user=request.user).account_number
        except UserWallet.DoesNotExist:
            account_number = request.data.get("account_number")


        amount = request.data.get("amount")
        number_to_pay_with = request.data.get("number_to_pay_with")

        if account_number and amount:

            result = utils.stk_push(phone=number_to_pay_with, amount=amount, accountReference=account_number)

            if result.get("ResponseCode") == "0":
                return Response(data=result, status=status.HTTP_200_OK)
            elif result.get("ResponseCode") == "500":
                return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data=result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        else:
            message = {
                "error": "please provide the account number"
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


class StkPushWebHookApiView(generics.GenericAPIView):
    
    def post(self, request):
        print(request.data, "stkpush webhook")
        data = request.data
        # call helper method to save transaction to db
        helpers.process_stk_hookdata(data)

        return Response(status=status.HTTP_200_OK)


class C2BTransactionListView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        # get all transacations that match the Userwallet from billrefnumber
        user_wallet = UserWallet.objects.get(user=request.user)
        transactions = C2BMpesaTransaction.objects.filter(billRefNumber=user_wallet.account_number)

        serializer = C2BMpesaTransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    


class C2BConfirmationView(generics.GenericAPIView):
    
    def post(self, request):
        data = request.data
        print(data, "confirmation")
        # call c2b helper to save trans to db

        message, status_code = helpers.process_c2b_confirmation_data(data)


        return Response(message, status=status_code)


class JointTransactionListView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        # get all transacations that match the Userwallet from billrefnumber
        try:
            user_wallet = UserWallet.objects.get(user=request.user)
        except UserWallet.DoesNotExist:
            message = {
                "wallet": "wallet for target user does not exist",
            }
            return Response(message, status=status.HTTP_404_NOT_FOUND)

        transactions = JointLmnC2BTransaction.objects.filter(target_accont=user_wallet.account_number)

        serializer = JointLmnC2BTransactionSerializer(transactions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)