from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from ..models import UserWallet, User

from django.db.utils import IntegrityError

class UserWalletModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="TestPassword"
        )
        cls.user2 = User.objects.create_user(
            username="testuser2",
            password="TestPassword2"
        )

        cls.user_wallet = UserWallet.objects.create(
            user=cls.user,
            account_number="254759288121",
        )


    def test_user_wallet_data(self):
        self.assertEqual(self.user_wallet.user, self.user)
        self.assertEqual(self.user_wallet.account_number, "254759288121")
        self.assertEqual(self.user_wallet.balance, 0.00)
    
    # test with a fail first
    def test_user_wallet_OneToOne_integrity(self):
        # test One to One Integrity Error by creating another wallet with the same user
        with self.assertRaises(Exception) as raised:  # top level exception as we want to figure out its exact type
            UserWallet.objects.create(
                user=self.user,
                account_number="254113953355",
            )
        # print(Exception)
        self.assertEqual(IntegrityError, type(raised.exception))

    def test_userWallet_accountNumber_integrity(self):
        # test account_number integrity Error by creating another wallet with the same account number
        with self.assertRaises(Exception) as raised:  # top level exception as we want to figure out its exact type
            UserWallet.objects.create(
                user=self.user2,
                account_number="254759288121",
            )
        # print(Exception)
        self.assertEqual(IntegrityError, type(raised.exception))