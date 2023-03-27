from decimal import Decimal
from rest_framework.test import APITestCase

from django.urls import reverse

from rest_framework import status

from ..mpesa import utils, helpers

class MpesaUtilsTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.account_number = "254113953355"

    def test_get_access_token(self):
        # test  will pass only if consumer key and secret is valid
        result = utils.get_access_token()
        self.assertEqual(result[1], status.HTTP_200_OK)

    def test_register_callbackurls(self):
        result = utils.register_callbackurls()
        self.assertEqual(result["ResponseCode"], '0')
        self.assertEqual(result["ResponseDescription"], 'Success')
        self.assertEqual(set(result.keys()), set(['OriginatorCoversationID', 'ResponseCode', 'ResponseDescription']))

    

    def test_simulate_c2b_transaction(self):
        result = utils.simulate_c2b_transaction(account_number=self.account_number, amount=1)
        # print(result)
        self.assertEqual(result["ResponseCode"], '0')
        self.assertEqual(result["ResponseDescription"], 'Accept the service request successfully.')
        self.assertEqual(set(result.keys()), set(['OriginatorCoversationID', 'ResponseCode', 'ResponseDescription']))

        # self.assertEqual(result["ShortCode"], '174379')
        # self.assertEqual(result["CommandID"], 'CustomerPayBillOnline')
        # self.assertEqual(result["Amount"], 1)
        # self.assertEqual(result["Msisdn"], '254708374149')
        # self.assertEqual(result["BillRefNumber"], self.account_number)


    
    def test_stk_push(self):
        result = utils.stk_push(phone="254113953355", amount=1, accountReference="254759288121")
        self.assertEqual(result["ResponseCode"], '0')
        self.assertEqual(result["ResponseDescription"], 'Success. Request accepted for processing')




