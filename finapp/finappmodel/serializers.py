from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db import connections


# serializer for creating user
class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','username','email','password','is_superuser','is_staff']
        extra_kwargs = {
        'username': {
            'error_messages': {
                'blank': 'Username should not be empty.',
                'required' : 'Username is mandatory.',
                'invalid' : 'Please enter the valid username.',
            }
        },
        'password' : {
            'error_messages':{
                'blank': 'Password should not be empty.',
                'required' : 'Password is mandatory.',
                'invalid' : 'Please enter the valid password.'
            }
        },
        'email' : {
            'error_messages':{
                'blank': 'Email ID should not be empty.',
                'required' : 'Email ID is mandatory.',
                'invalid' : 'Please enter the valid email address.'
            }
        },
        
    }


# serilizer for create user profile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
