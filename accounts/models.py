from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class UserWallet(models.Model):
    # one user can have only one wallet
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    # start balance with default of 0
    balance = models.DecimalField(default=0.00, decimal_places=2, max_digits=10)

    def __str__(self):
        return f"{self.user.username} account"