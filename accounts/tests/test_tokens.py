from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from ..models import User

class WalletUtilsTestCase(TestCase):
    # test if function modifies the wallet 

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="TestPassword"
        )

        cls.valid_login_credentials = {
            "username":"testuser",
            "password":"TestPassword"
        }

        cls.expired_refresh_token =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3OTcyMTY3NywiaWF0IjoxNjc5NjM1Mjc3LCJqdGkiOiIxOTliNjhjMmUzMDE0YWRjYjg1YjUxODc1MWQ0MjJlZCIsInVzZXJfaWQiOjF9.48xdcVVVwWbLK-Mgcqga0N9w8prirfI6-htwsQ5d_DU"


    def test_access_token_api(self):
        # start with false credentials
        response = self.client.post(
            reverse("token_obtain_pair"),
            data={
                "username": "ssjsjdf",
                "password": "sajskjdkla"
            }
        )
        json_response = response.json()
        # print(json_response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(set(json_response.keys()), set(["detail"]))
        self.assertEqual(json_response.get('detail'), 'No active account found with the given credentials')

        # test with valid credentials
        response = self.client.post(
            reverse("token_obtain_pair"),
            data=self.valid_login_credentials
        )
        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(json_response.keys()), set(["access", "refresh"]))


    
    def test_refresh_token_api(self):
        # start with invalid refresh token
        response = self.client.post(
            reverse("token_refresh"),
            data={
                "refresh": "invalidrefreshtoken",
            }
        )
        json_response = response.json()
        # print(json_response)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(set(json_response.keys()), set(["detail", "code"]))
        self.assertEqual(json_response.get('detail'), "Token is invalid or expired")
        self.assertEqual(json_response.get('code'), "token_not_valid")

        # test expired refresh token
        response = self.client.post(
            reverse("token_refresh"),
            data={
                "refresh": self.expired_refresh_token,
            }
        )
        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(set(json_response.keys()), set(["detail", "code"]))
        self.assertEqual(json_response.get('detail'), "Token is invalid or expired")
        self.assertEqual(json_response.get('code'), "token_not_valid")


        # test with valid refresh token
        response = self.client.post(
            reverse("token_obtain_pair"),
            data=self.valid_login_credentials
        )
        refresh_token = response.json()["refresh"]

        response = self.client.post(
            reverse("token_refresh"),
            data={
                "refresh": refresh_token
            }
        )

        json_response = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(set(json_response.keys()), set(["access"]))
