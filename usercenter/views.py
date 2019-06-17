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
from college.models import ClassInfo
from college.serializers import GlassSerializer
from dormitory.models import DormBuild
from dormitory.serializers import BuildSerializer
from .serializers import *
from .permissions import *
from .models import *

# base
import logging
import json
import jwt


logger = logging.getLogger('sourceDns.webdns.views')

# Create your views here.
class UserLogin(APIView):

    # def get(self,request):
    #     # token = request.META.get("HTTP_AUTHORIZATION").split(' ')
    #     # tokenstr = str.encode(token[2])
    #     # a = jwt.decode(tokenstr, 'secret_key', algorithms=['HS256'])
    #     token = request.META.get("HTTP_AUTHORIZATION").split(' ')
    #     trole = jwt_decode_handler(token[2])
    #     return

    def post(self,request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == "" or password == "":
            result = False
            data = ""
            error = "用户名密码不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user = authenticate(username=username, password=password)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "用户名密码不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
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
            data = {}
            data['user'] = user.username
            data['role'] = user.role
            data['retoken'] = token
            result = True
            data = data
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})


# 超级管理员对基础设施管理员的账号管理
class SuperBaseView(APIView):

    def get(self, request):
        user_2_all = UserInfo.objects.filter(role=2)
        user_data = UserSerializer(user_2_all, many=True)
        user_data = user_data.data
        result = True
        data = user_data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        old_user = UserInfo.objects.filter(username=username)
        if old_user:
            result = False
            data = ""
            error = "用户名不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        new_password = make_password(password, None, 'pbkdf2_sha1')
        try:
            user = UserInfo.objects.create(username=username, password=new_password, role=2)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "基础设施管理员" + user.username + "添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "基础设施管理员" + user.username + "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


    def put(self, request):
        username = request.data.get("username", "")
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        if username == "" or old_password == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=2)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(old_password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=2)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user.delete()
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "基础设施管理员" + user[0].username + "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


# 超级管理员对学校管理员的账号管理
class SuperSchoolView(APIView):

    def get(self, request):
        user_1_all = UserInfo.objects.filter(role=1)
        user_data = UserSerializer(user_1_all, many=True)
        user_data = user_data.data
        result = True
        data = user_data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        old_user = UserInfo.objects.filter(username=username)
        if old_user:
            result = False
            data = ""
            error = "用户名不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        new_password = make_password(password, None, 'pbkdf2_sha1')
        try:
            user = UserInfo.objects.create(username=username, password=new_password, role=1)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "学校管理员" + user.username + "添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "学校管理员" + user.username + "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        username = request.data.get("username", "")
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        if username == "" or old_password == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=1)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(old_password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=1)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user.delete()
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "基础设施管理员" + user[0].username + "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


# 超级管理员对宿舍管理员的账号管理
class SuperDormView(APIView):

    def get(self, request):
        user_4_all = UserInfo.objects.filter(role=4)
        build_list = list()
        for user in user_4_all:
            data = {}
            user_data = UserSerializer(user, many=False)
            user_data = user_data.data
            build = DormBuild.objects.filter(manager=user)
            build_data = BuildSerializer(build, many=True)
            build_data = build_data.data
            data["user_data"] = user_data
            data["build_data"] = build_data
            build_list.append(data)
        result = True
        data = build_list
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        build_id = request.POST.get("build_id", "")
        if username == '' or password == '' or build_id == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        old_user = UserInfo.objects.filter(username=username)
        if old_user:
            result = False
            data = ""
            error = "用户名不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        build = DormBuild.objects.filter(id=build_id)
        if not build:
            result = False
            data = ""
            error = "请输入正确宿舍楼信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        new_password = make_password(password, None, 'pbkdf2_sha1')
        try:
            user = UserInfo.objects.create(username=username, password=new_password, role=4)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "宿舍管理员" + user.username + "添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            build.update(manager=user)
        except ObjectDoesNotExist as e:
            logger.error(e)
            user.delete()
            result = False
            data = ""
            error = "宿舍管理员" + user.username + "添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "宿舍管理员" + user.username + "添加并绑定成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        username = request.data.get("username", "")
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        if username == "" or old_password == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=4)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(old_password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=4)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user.delete()
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "宿舍管理员" + user[0].username + "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


# 超级管理员对导员的账号管理
class SuperGuideView(APIView):

    def get(self, request):
        user_3_all = UserInfo.objects.filter(role=3)
        class_list = list()
        for user in user_3_all:
            data = {}
            user_data = UserSerializer(user, many=False)
            user_data = user_data.data
            class_info = ClassInfo.objects.filter(guide=user)
            class_data = GlassSerializer(class_info, many=True)
            class_data = class_data.data
            data["user_data"] = user_data
            data["class_data"] = class_data
            class_list.append(data)
        result = True
        data = class_list
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        old_user = UserInfo.objects.filter(username=username)
        if old_user:
            result = False
            data = ""
            error = "用户名不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        new_password = make_password(password, None, 'pbkdf2_sha1')
        try:
            user = UserInfo.objects.create(username=username, password=new_password, role=3)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "导员" + user.username + "添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "导员" + user.username + "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        username = request.data.get("username", "")
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        if username == "" or old_password == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=3)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(old_password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        if username == '' or password == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(username=username, role=3)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        if not check_password(password, user[0].password):
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            user.delete()
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "宿舍管理员" + user[0].username + "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})










