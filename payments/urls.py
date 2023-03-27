from django.urls import path

from .views import (
    C2BValidationView,
    C2BConfirmationView, 
    RegisterMpesaCallBackUrlsView, 
    SimulateC2BTransactionView, 
    C2BTransactionListView,
    StkPushProcessApiView,
    StkPushWebHookApiView,
    JointTransactionListView,
)

urlpatterns = [
    # callback hooks
    path('c2b_validation_hook', C2BValidationView.as_view(), name="c2b_validation"),
    path('c2b_confirmation_hook', C2BConfirmationView.as_view(), name="c2b_confirmation"),
    path('stk_push_webhook', StkPushWebHookApiView.as_view(), name="stk_push_webhook"),


    # register mpesa validation and confirmation url
    path('register_c2b_mpesa_callbackurls', RegisterMpesaCallBackUrlsView.as_view(), name="register_mpesa_callbackUrls"),
    path('simulate_c2b_transaction', SimulateC2BTransactionView.as_view(), name="c2b_transaction_simulate"),
    path('stk_push_process', StkPushProcessApiView.as_view(), name="stk_push_process"),
    path('c2btransaction/list', C2BTransactionListView.as_view(), name="transaction_list_view"),

    path('joint_transactions/list', JointTransactionListView.as_view(), name="joint_transaction_list_view"),

]