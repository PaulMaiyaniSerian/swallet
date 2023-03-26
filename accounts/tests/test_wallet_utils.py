from django.test import TestCase
from ..wallet import utils
from ..models import User, UserWallet

class WalletUtilsTestCase(TestCase):
    # test if function modifies the wallet 

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
    
    def test_add_to_wallet_util(self):
        # shoud have balance of 0
        self.assertEqual(self.user_wallet.balance, 0)
        # update balance
        wallet_obj = utils.add_to_wallet(self.user_wallet.account_number, 100.00)
        # check new balance
        self.assertEqual(wallet_obj.balance, 100.00)

        # check add wallet of an account number that does not exist
        invalid_wallet = utils.add_to_wallet("invalid-account-number", 100.00)
        self.assertEqual(invalid_wallet, None)



       