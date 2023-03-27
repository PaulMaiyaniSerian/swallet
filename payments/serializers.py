from rest_framework import serializers

from .models import C2BMpesaTransaction, LNMTransaction, JointLmnC2BTransaction

class C2BMpesaTransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = C2BMpesaTransaction
        fields = "__all__"

class LNMTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LNMTransaction
        fields = "__all__"

class JointLmnC2BTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = JointLmnC2BTransaction
        fields = "__all__"


class C2BMpesaTransactionViewSerializer(serializers.Serializer):
    account_number = serializers.CharField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)

class StkPushSerializer(serializers.Serializer):
    number_to_pay_with= serializers.CharField()
    amount = serializers.DecimalField(decimal_places=2, max_digits=10)