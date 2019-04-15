# restful API
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_decode_handler

#django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse,request
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import login,authenticate

# selfproject
from .serializers import *
from .permissions import *
from .models import *

# base
import logging
import json
import jwt

# Create your views here.
class UserLogin(APIView):

    def get(self,request):
        # token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        # tokenstr = str.encode(token[2])
        # a = jwt.decode(tokenstr, 'secret_key', algorithms=['HS256'])
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        trole = jwt_decode_handler(token[2])
        print(trole)


    def post(self,request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            result = False
            data = ""
            error = "用户名密码不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user = authenticate(username=username,password=password)
            if user:

                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                logininfo = jwt_payload_handler(user)
                logininfo['role'] = user.role
                token = jwt_encode_handler(logininfo)
                # logininfo={}
                # logininfo["userid"]=user.id
                # logininfo["username"]=user.username
                # logininfo["role"]=user.role
                # encoded_jwt = jwt.encode(logininfo, 'secret_key',algorithm='HS256')
                # encoded_jwt = bytes.decode(encoded_jwt)
                data={}
                data['user'] = user.username
                data['token'] = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoyLCJ1c2VybmFtZSI6InFxIiwicm9sZSI6MywiZXhwIjoxNTU1MzQ5ODQwLCJlbWFpbCI6IiJ9.vQZRrKst50GBerLjroHUP-sxed0WjSBgQIApd7saEhI'
                result = True
                data = data
                error = ""
                return JsonResponse({"result": result, "data": data, "error": error})

        except ObjectDoesNotExist as e:
            logging.warning(e)