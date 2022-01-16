from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from backend.serializers import UserSerializer
from backend.models import User
from backend import serializers

class LoginView(APIView):
    pass



class SignUp(APIView):
    def create(self, request, *args, **kwargs):
        serializer = UserSerializer
    
    
        return Response(serializers.data)



class PermissionUp(APIView):
    pass