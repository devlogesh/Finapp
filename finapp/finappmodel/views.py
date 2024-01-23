from django.shortcuts import render
from .serializers import *
from .models import *

from rest_framework.views import APIView
from rest_framework import status, generics,filters
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .functions import *
# Create your views here.


class UserSignup(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        data = user_parser(request)
        print(data,"DATA")
        token_key = request.META.get('HTTP_AUTHORIZATION')
        if 'access_key' in request.data:
            print(request.data['access_key'],"request.data['access_key']")
            if request.data['access_key'] != "SelmuruganBondamani":
                return Response({'message':'Access Key Mismatch'},status=status.HTTP_400_BAD_REQUEST)
            user_params = user_parser(request)
        elif token_key:
            user_params = user_parser(request)
        else:
            return Response({"message":"Access Key or Token Must"},status=status.HTTP_400_BAD_REQUEST)
        user_serializer = UserCreateSerializer(data=user_params['user'])
        if user_serializer.is_valid():
            user = User.objects.create(**user_serializer.validated_data)
            user.set_password(user_params['user']['password'])
            user.save()
            user_id = user.id
            user_params['profile']['user_id'] = user_id
            user_params['profile']['code'] = "EX123"
            
            profile_serializer = UserProfileSerializer(data=user_params['profile'])
            if profile_serializer.is_valid():
                profile = UserProfile.objects.create(**profile_serializer.validated_data)
                
                profile.save()
                return Response({'username':user.username,'message':'User Created Successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({"error":profile_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":user_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
            


