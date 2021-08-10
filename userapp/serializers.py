from rest_framework import serializers

from .serializers import *
from .models import *


class AccountRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['username', 'password', 'email', 'is_authority', 'is_customer']
         # password will not be render with the user
        extra_kwargs = {'password': {'write_only': True}}
    
    # override create method for password hashing
    def create(self, validated_data):

        user = Account(
            username= validated_data['username'],
            email = validated_data['email'],
            is_authority = validated_data.get('is_authority', False),
            is_customer = validated_data.get('is_customer', False)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

