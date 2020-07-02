from rest_framework import serializers
from .models import Total
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class CreateTotalSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user')

    class Meta:
        model = Total
        fields = ("initial_amount","total_amount","total_amount_gained","total_amount_spent", "user")

    def get_user(self, total):
        user = total.user
        return user
    
    def create(self, validated_data):
        return Total.objects.create(**validated_data)


class TotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Total
        fields = "__all__"
        

            
