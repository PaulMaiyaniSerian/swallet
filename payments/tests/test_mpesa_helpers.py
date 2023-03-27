from decimal import Decimal
from rest_framework.test import APITestCase

from django.urls import reverse

from rest_framework import status

from accounts.models import User, UserWallet

from ..mpesa import  helpers

class MpesaUtilsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="TestPassword"
        )

        # create an account with the user
        cls.user_wallet = UserWallet.objects.create(
            user=cls.user,
            account_number="254759288121"
        )

        cls.c2b_sample_response = {
            'TransactionType': 'Pay Bill', 
            'TransID': 'RCO41MKB14', 
            'TransTime': '20230324103853', 
            'TransAmount': '1.00', 
            'BusinessShortCode': '174379', 
            'BillRefNumber': '254113953355', 
            'InvoiceNumber': '', 
            'OrgAccountBalance': '943728.00', 
            'ThirdPartyTransID': '', 
            'MSISDN': 'bbff37cea44ac0b2d964ee0dfb8d2df8513dc7ba1b36129a929fc3fbd6dd4af4', 
            'FirstName': 'John', 
            'MiddleName': '', 
            'LastName': ''
        }

        
        

        cls.stk_hook_sample_response = {
                'Body': {
                    'stkCallback': {
                        'MerchantRequestID': '3786-9664944-1',
                        'CheckoutRequestID': 'ws_CO_24032023165155703113953355', 
                        'ResultCode': 0, 
                        'ResultDesc': 'The service request is processed successfully.', 
                        'CallbackMetadata': {
                            'Item': [
                                {'Name': 'Amount', 'Value': 1.0}, 
                                {'Name': 'MpesaReceiptNumber', 'Value': 'RCO4JCX8AW'}, 
                                {'Name': 'Balance'}, 
                                {'Name': 'TransactionDate', 'Value': 20230324165208}, 
                                {'Name': 'PhoneNumber', 'Value': 2547113955555 }]
                        }
                    }
                }
            }
        

    def test_process_stk_hookdata(self):
        result = helpers.process_stk_hookdata(self.stk_hook_sample_response)
        # result returning none means no exception
        self.assertEqual(result, None)