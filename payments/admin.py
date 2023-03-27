from django.contrib import admin

# Register your models here.
from .models import C2BMpesaTransaction, LNMTransaction, JointLmnC2BTransaction

class MpesaTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "billRefNumber",
        "transAmount",
        "transID", 
        "transTime", 
        "firstName" 
    ]


admin.site.register(C2BMpesaTransaction, MpesaTransactionAdmin)

class LNMTransactionsAdmin(admin.ModelAdmin):
    list_display = [
        "checkoutRequestID", 
        "merchantRequestID", 
        "amount",
        "phoneNumber",
        "transactionDate", 
        "mpesaReceiptNumber",
        "resultDesc",
        "target_account"
    ]

admin.site.register(LNMTransaction, LNMTransactionsAdmin)

class JointLmnC2BTransactionAdmin(admin.ModelAdmin):
    list_display = [
        "mpesa_code", 
        "amount", 
        "target_accont",
        "type",
        "transaction_time", 
    ]

admin.site.register(JointLmnC2BTransaction, JointLmnC2BTransactionAdmin)