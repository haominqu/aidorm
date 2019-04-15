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


# selfproject
from .serializers import *
from .permissions import *
from .models import *

# base
import logging
import json


# Create your views here.
class UserLogin(APIView):

    def get(self,request):
        pass
    def post(self,request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            result = False
            data = ""
            error = "用户名密码不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user = UserInfo.objects.get(username=username)
            userpwd = check_password(password, user.userpwd)
            if userpwd:
                jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
                jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
                logininfo = jwt_payload_handler(user)
                logininfo['role'] = user.role
                token = jwt_encode_handler(logininfo)
                data={}
                data['co    user'] = user.username
                data['token'] = token
                result = True
                data = data
                error = ""
                return JsonResponse({"result": result, "data": data, "error": error})

        except ObjectDoesNotExist as e:
            logging.warning(e)