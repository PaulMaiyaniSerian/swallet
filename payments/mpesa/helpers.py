import decimal

from payments.models import LNMTransaction
from accounts.models import UserWallet
from payments.models import C2BMpesaTransaction
from accounts.wallet import utils as wallet_utils
from rest_framework import status

def process_stk_hookdata(data):
    # format and save to db
    merchantRequestID = data["Body"]["stkCallback"]["MerchantRequestID"]
    checkoutRequestID = data["Body"]["stkCallback"]["CheckoutRequestID"]
    resultCode = data["Body"]["stkCallback"]["ResultCode"]
    resultDesc = data["Body"]["stkCallback"]["ResultDesc"]

    # use result code to check if cancelled or success
    # cancelled payment

    if resultCode == 1032:
        try:
            # get the transaction with merchid and checkoutid
            lnm_transaction = LNMTransaction.objects.get(
                merchantRequestID=merchantRequestID,
                checkoutRequestID=checkoutRequestID,
            )
            # update the trans
            lnm_transaction.resultCode = resultCode
            lnm_transaction.resultDesc = resultDesc
            lnm_transaction.save()

        except LNMTransaction.DoesNotExist:
            pass

        
    elif resultCode == 0:
        # success payment
        merchantRequestID = data["Body"]["stkCallback"]["MerchantRequestID"]
        checkoutRequestID = data["Body"]["stkCallback"]["CheckoutRequestID"]
        resultCode = data["Body"]["stkCallback"]["ResultCode"]
        resultDesc = data["Body"]["stkCallback"]["ResultDesc"]

        amount = ""
        mpesaReceiptNumber = ""
        balance = ""
        transactionDate = ""
        phoneNumber = ""

        callbackMetadataItems = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
        for item in callbackMetadataItems:
            if item["Name"] == "Amount":
                amount = item["Value"]
            elif item["Name"] == "MpesaReceiptNumber":
                mpesaReceiptNumber = item["Value"]
            elif item["Name"] == "Balance":
                balance = ""
            elif item["Name"] == "TransactionDate":
                transactionDate = item["Value"]
            elif item["Name"] == "PhoneNumber":
                phoneNumber = item["Value"]
        
        # update transaction
        try:
            # get the transaction with merchid and checkoutid
            lnm_transaction = LNMTransaction.objects.get(
                merchantRequestID=merchantRequestID,
                checkoutRequestID=checkoutRequestID,
            )
            # update the trans
            lnm_transaction.resultCode = resultCode
            lnm_transaction.resultDesc = resultDesc
            lnm_transaction.amount = amount
            lnm_transaction.mpesaReceiptNumber = mpesaReceiptNumber
            lnm_transaction.balance = balance
            lnm_transaction.transactionDate = transactionDate
            lnm_transaction.phoneNumber = phoneNumber

            lnm_transaction.save()

            # get acccount from target_account in lnmTransaction
            # use the wallet helper function to add to balance
            wallet_utils.add_to_wallet(
                account_number=lnm_transaction.target_account, 
                amount=lnm_transaction.amount
            )
            # user_wallet = UserWallet.objects.get(account_number=lnm_transaction.target_account)
            # user_wallet.balance += decimal.Decimal(lnm_transaction.amount)
            # user_wallet.save()

        except LNMTransaction.DoesNotExist:
            # print("error data does not exist")
            pass

    else:
        print("another result code received")


def process_c2b_confirmation_data(data):
    
     # create the transaction
    mpesa_transaction = C2BMpesaTransaction.objects.create(
        transactionType = data.get("TransactionType"),
        transID = data.get("TransID"),
        transTime = data.get("TransTime"),
        transAmount = data.get("TransAmount"),
        businessShortCode = data.get("BusinessShortCode"),
        billRefNumber = data.get("BillRefNumber"),
        invoiceNumber = data.get("InvoiceNumber"),
        orgAccountBalance = data.get("OrgAccountBalance"),
        thirdPartyTransID = data.get("ThirdPartyTransID"),
        mSISDN = data.get("MSISDN"),
        firstName = data.get("FirstName"),
        middleName = data.get("MiddleName"),
        lastName = data.get("LastName"),  
    )
    # update the user account balance from the billrefnumber

    try:
        user_wallet = UserWallet.objects.get(account_number=mpesa_transaction.billRefNumber)
    except UserWallet.DoesNotExist:
        message = {
            "account_number": "account with given number does not exist"
        }
        return (message, status.HTTP_400_BAD_REQUEST)


    # add to balance
    user_wallet.balance += decimal.Decimal(mpesa_transaction.transAmount)
    user_wallet.save()

    success_message = {
        "success": "transaction saved successfully"
    }

    return (success_message, status.HTTP_200_OK)