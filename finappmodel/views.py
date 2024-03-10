from django.shortcuts import render
from .serializers import *
from .models import *

from rest_framework.views import APIView
from rest_framework import status, generics,filters
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate,login

from .functions import *
# Create your views here.


class UserSignup(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        token_key = request.META.get('HTTP_AUTHORIZATION')
        user_params = user_parser(request)
        if len(user_params['profile']['mobile']) != 10:
            return Response({"message":"Mobile No. length Should be 10"},status=status.HTTP_400_BAD_REQUEST)
        user_serializer = UserCreateSerializer(data=user_params['user'])
        if user_serializer.is_valid():
            user = User.objects.create(**user_serializer.validated_data)
            user.set_password(user_params['user']['password'])
            user.save()
            user_id = user.id
            user_params['profile']['user_id'] = user_id
            user_params['profile']['code'] = "EX1231"
            
            profile_serializer = UserProfileSerializer(data=user_params['profile'])
            if profile_serializer.is_valid():
                profile = UserProfile.objects.create(**profile_serializer.validated_data)
                
                profile.save()
                return Response({'username':user.username,'message':'User Created Successfully'},status=status.HTTP_201_CREATED)
            else:
                return Response({"error":profile_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error":user_serializer.errors},status=status.HTTP_400_BAD_REQUEST)


class LoginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        request_data = request.data      
        username = request_data.get('username')
        password = request_data.get('password')
        if username and password:
            user = authenticate(username=username,password=password)
            if user:
                profile = UserProfile.objects.filter(user_id=user.id)
                if len(profile) == 0:
                    return Response({"messge":"UserProfile is not mapped for this User"},status=status.HTTP_400_BAD_REQUEST)
                else:
                    login(request,user)
                    token_id = Token.objects.filter(user_id = user.id)
                    if len(token_id)>0:
                        token_id.delete()
                    token,create = Token.objects.get_or_create(user=user)
                    access_token = AccessToken.objects.create(user_id=user
                    ,key=token.key,created_by_id=profile[0],updated_by_id=profile[0])
                    serializer = UserProfileSerializer(profile[0])
                    serializer_dict = serializer.data
                    serializer_dict['token_key'] = token.key
                    serializer_dict['address'] = {'line1': serializer_dict['address_line1'],'line2': serializer_dict['address_line2'],'street': serializer_dict['street'],'city': serializer_dict['city'],'district': serializer_dict['district'], 'state': serializer_dict['state'], 'country': serializer_dict['country'], 'zipCode': serializer_dict['pincode']}
                    del serializer_dict['address_line1']
                    del serializer_dict['address_line2']
                    del serializer_dict['street']
                    del serializer_dict['city']
                    del serializer_dict['district']
                    del serializer_dict['state']
                    del serializer_dict['country']
                    del serializer_dict['pincode']

                    return Response(serializer_dict,status=status.HTTP_200_OK)

            else:
                return Response({"messge":"username or password is incorrect"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"messge":"please provide username and password"},status=status.HTTP_400_BAD_REQUEST)