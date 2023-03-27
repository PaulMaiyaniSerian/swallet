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
