from decimal import Decimal
from rest_framework.test import APITestCase

from django.urls import reverse

from rest_framework import status

from ..models import User, UserWallet

class AccountBalanceApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        # create user 
        # get token
        # get balance
        cls.user = User.objects.create_user(
            username="testuser",
            password="TestPassword"
        )

        # create an account with the user
        cls.user_wallet = UserWallet.objects.create(
            user=cls.user,
            account_number="254759288121"
        )


    
    def test_account_balance_api(self):
        # force auth the user
        self.client.force_authenticate(self.user)

        # call the balance apiview
        response = self.client.get(
            path=reverse("wallet_balance")
        )

        json_response = response.json()
        balance = json_response.get("balance")

        # balance check for first create
        self.assertEqual(balance, "0.00")

        # move to walletutils
        # # modify balance and check again
        # self.user_wallet.balance += 10
        # self.user_wallet.save()

        # self.assertEqual(self.user_wallet.balance, 10.00)
        # # check if the id of user is same as the users wallet user id
        # self.assertEqual(self.user.id, self.user_wallet.user.id)
