# from django.test import TestCase
from rest_framework.test import APITestCase

from django.urls import reverse

from rest_framework import status

from ..models import UserWallet
# Create your tests here.
class RegisterApiTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_credentials = {
            "username": "testuser1",
            "password": "StrongPassword",
            "password2": "StrongPassword",
            "phone": "254759288121"
        }

        cls.duplicate_acccountNum_credentials = {
            "username": "testuser3",
            "password": "StrongPassword",
            "password2": "StrongPassword",
            "phone": "254759288121"
        }

        cls.duplicate_username_credentials = {
            "username": "testuser1",
            "password": "StrongPassword",
            "password2": "StrongPassword",
            "phone": "254759288122"
        }

        cls.weak_password_credentials = {
            "username": "testuser2",
            "password": "1234",
            "password2": "1234",
            "phone": "254759288123"
        }

        cls.unmatched_password_credentials = {
            "username": "testuser2",
            "password": "StrongPassword",
            "password2": "UnmatchedPass2",
            "phone": "254759288123"
        }

        cls.invalid_phone_credentials = {
            "username": "testuser2",
            "password": "StrongPassword",
            "password2": "StrongPassword",
            "phone": "25475928812323"
        }

        

        

    def test_register_view(self):
        response = self.client.post(
            path=reverse("register_normal_user"),
            data=self.user_credentials
        )
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        # should return username since the rest of the fields are write only
        self.assertEqual(response.json(),{"username": "testuser1"})


    # ToDo:

    # start test username uniqueness
    def test_register_view_username_uniqueness(self):
        response = self.client.post(
            path=reverse("register_normal_user"),
            data=self.user_credentials
        )

        response_2 = self.client.post(
            path=reverse("register_normal_user"),
            data=self.duplicate_username_credentials
        )
        # 201 for first response
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.json(),{"username": "testuser1"})

        # fail for response 2
        self.assertNotEqual(response_2.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code,status.HTTP_400_BAD_REQUEST)
        json_response = response.json()
        # error of type "password": [] should be present
        self.assertEqual(set(json_response.keys()), set(['username']))


    def test_register_view_password_validation(self):
       
        # response = 
        response = self.client.post(
            path=reverse("register_normal_user"),
            data=self.weak_password_credentials
        )
        self.assertNotEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        json_response = response.json()
        # error of type "password": [] should be present
        self.assertEqual(set(json_response.keys()), set(['password']))
    
    # start test account number uniqueness
    def test_register_view_accountNum_uniqueness(self):
        response = self.client.post(
            path=reverse("register_normal_user"),
            data=self.user_credentials
        )

        response_2 = self.client.post(
            path=reverse("register_normal_user"),
            data=self.duplicate_acccountNum_credentials
        )

        # 201 for first response
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response.json(),{"username": "testuser1"})

        # fail for response 2
        self.assertNotEqual(response_2.status_code,status.HTTP_201_CREATED)
        self.assertEqual(response_2.status_code,status.HTTP_400_BAD_REQUEST)
        json_response = response_2.json()
        # error for "phone" field : [] should be present
        self.assertEqual(set(json_response.keys()), set(['phone']))
    

    def test_passwords_match(self):
        response = self.client.post(
            path=reverse("register_normal_user"),
            data=self.unmatched_password_credentials
        )
        json_response = response.json()

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json_response.keys()), set(['password']))

    # check if phone has 12characters
    def test_phone_validity(self):
        response = self.client.post(
            path=reverse("register_normal_user"),
            data=self.invalid_phone_credentials
        )
        json_response = response.json()

        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        self.assertEqual(set(json_response.keys()), set(['phone']))



    