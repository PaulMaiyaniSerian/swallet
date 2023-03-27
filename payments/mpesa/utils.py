import requests
from datetime import datetime
import base64
import json
from requests.auth import HTTPBasicAuth

from requests.exceptions import ConnectionError

from django.conf import settings
from ..models import LNMTransaction
from rest_framework import status

CONNECTION_ERROR_RESPONSE = {
        "requestId": None,
        "errorMessage": "Service is temporarily not available.Please try again later.(Internet Connection)",
        "errorCode": "500"
    }
TOKEN_ERROR_RESPONSE = {
    "requestId": None,
    "errorMessage": "Invalid Consumer key and secret",
    "errorCode": "500"
}

def get_access_token():
    consumer_key = settings.CONSUMER_KEY
    consumer_secret = settings.CONSUMER_SECRET

    url = settings.MPESA_AUTH_URL

    try:
        response = requests.get(url, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        if response.status_code == 400:
            message = {
                "token": "invalid consumer key or secret"
            }
            return (message, status.HTTP_400_BAD_REQUEST)
        else:
            return (response.json(), status.HTTP_200_OK)
    
    # if cannot connect to safaricom return None
    except ConnectionError:
        return None



def register_callbackurls():
    token_response = get_access_token()

    if token_response[1] == status.HTTP_400_BAD_REQUEST:
        return TOKEN_ERROR_RESPONSE
    
    access_token_message, _ = token_response
    access_token = access_token_message["access_token"]

    url = settings.MPESA_REGISTER_CALLBACK_URL
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    data = {
        "ShortCode": settings.SHORTCODE,
        "ResponseType": "Completed",
        "ConfirmationURL": settings.CONFIRMATIONURL,
        "ValidationURL": settings.VALIDATIONURL,
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        # print(response.json())
        return (response.json())
    except ConnectionError:
        return CONNECTION_ERROR_RESPONSE


def stk_push(phone, amount, accountReference):

    token_response = get_access_token()

    if token_response[1] == status.HTTP_400_BAD_REQUEST:
        return TOKEN_ERROR_RESPONSE
    
    access_token_message, _ = token_response
    access_token = access_token_message["access_token"]


    url = settings.PROCESS_STKPUSH_URL
    businessShortCode = settings.SHORTCODE
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    transaction_type = "CustomerPayBillOnline"
    CallBackURL = settings.STKPUSH_CALLBACKURL
    passkey = settings.PASSKEY
    data_to_encode = businessShortCode + passkey + timestamp

    
    online_password = base64.b64encode(data_to_encode.encode())
    decoded_password = online_password.decode('utf-8')

    headers = {"Authorization": f"Bearer {access_token}"}

    data = {
        "BusinessShortCode": businessShortCode,
        "Password": decoded_password,
        "Timestamp": timestamp,
        "TransactionType": transaction_type,
        "Amount": amount,
        "PartyA": phone,
        "PartyB": businessShortCode,
        "PhoneNumber": phone,
        "CallBackURL": CallBackURL,
        "AccountReference": accountReference,
        "TransactionDesc": "Payment to Swallet"
    }
    
    try:
        '''
        if response code == 0 then it is succesful and we can add 
        merchant id and checkout id plus target_account
        to the transactions which will later be modified in callback hook
        '''
    
        response = requests.post(url, json=data, headers=headers)
        json_response = response.json()
        if json_response.get("ResponseCode") == "0":
            print("successfuly sent")
            LNMTransaction.objects.create(
                merchantRequestID=json_response["MerchantRequestID"],
                checkoutRequestID=json_response["CheckoutRequestID"],
                target_account=accountReference
            )
        return response.json()
    
    except ConnectionError:
        return CONNECTION_ERROR_RESPONSE

   


# function to simulate payment
# todo add serializer for amount
def simulate_c2b_transaction(account_number, amount):
    # bill refnumber is target account to add the funds to
    token_response = get_access_token()

    if token_response[1] == status.HTTP_400_BAD_REQUEST:
        return TOKEN_ERROR_RESPONSE
    
    access_token_message, _ = token_response
    access_token = access_token_message["access_token"]

    url = settings.C2B_SIMULATE_URL

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    data = {
        "ShortCode": int(settings.SHORTCODE),
        "CommandID": "CustomerPayBillOnline",
        "Amount": int(amount),
        "Msisdn": int(settings.TESTMSISDN),
        "BillRefNumber": account_number
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except ConnectionError:
        return CONNECTION_ERROR_RESPONSE


# simulate_c2b_transaction("254711393355", "12")'
