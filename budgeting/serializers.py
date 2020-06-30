from rest_framework import serializers
from budgeting.models import *


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total
        fields = '__all__'


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
