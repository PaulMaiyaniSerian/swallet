from rest_framework import serializers

from .models import C2BMpesaTransaction, LNMTransaction

class C2BMpesaTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = C2BMpesaTransaction
        fields = "__all__"

class LNMTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMTransaction
        fields = "__all__"