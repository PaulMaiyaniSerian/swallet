from ..models import  UserWallet
import decimal

# create function to modify wallet balance 
def add_to_wallet(account_number, amount):
    # get user wallet
    try:
        user_wallet = UserWallet.objects.get(account_number=account_number)
        user_wallet.balance += decimal.Decimal(amount)
        user_wallet.save()
        return user_wallet
    
    except UserWallet.DoesNotExist:
        return None
