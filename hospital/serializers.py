from rest_framework import serializers
from django.contrib.auth.models import User

from hospital.models import *


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
         # password will not be render with the user
        extra_kwargs = {'password': {'write_only': True}}
    
    # override create method for password hashing
    def create(self, validated_data):

        user = User(
            username= validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


