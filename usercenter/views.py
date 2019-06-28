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
from django.db.models import Q

# selfproject
from college.models import ClassInfo, Major
from college.serializers import GlassSerializer

from dormitory.models import DormBuild,AccessRecords
from dormitory.serializers import BuildSerializer, UnboundBuildSerializer,AccessRecordSerializer

from dormitory.models import DormBuild, DormRoom, BedNumber, FaceMachine
from dormitory.serializers import BuildSerializer, UnboundBuildSerializer, Student
from student.models import StudentDetail

from .serializers import *
from .permissions import *
from .models import *
from aidorm.settings import BASE_URL



# base
import logging
import json
import jwt
import datetime
import time


logger = logging.getLogger('sourceDns.webdns.views')

# Create your views here.

# 验证用户携带token的装饰器
def login_decorator(func):
    def token_func(request, *args, **kwargs):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            result = False
            data = ""
            error = "token无效"
            return JsonResponse({"result": result, "data": data, "error": error})
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        token_dict = jwt_decode_handler(token[2])
        return func(token_dict)
    return token_func


# 最近操作记录装饰器
# def operation_decorator(func):
#     def log_addition(request, *args, **kwargs):





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
        user = UserInfo.objects.filter(username=username)
        if not user:
            result = False
            data = ""
            error = "未查询到用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        is_pwd = check_password(password, user[0].password)
        if not is_pwd:
            result = False
            data = ""
            error = "用户名密码不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        if user:
            if user[0].last_login:
                user.update(recent_time=user[0].last_login)
                now_time = datetime.datetime.now()
                user.update(last_login=now_time)
            else:
                now_time = datetime.datetime.now()
                user.update(last_login=now_time)
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            logininfo = jwt_payload_handler(user[0])
            logininfo['role'] = user[0].role
            token = jwt_encode_handler(logininfo)
            # logininfo={}
            # logininfo["userid"]=user.id
            # logininfo["username"]=user.username
            # logininfo["role"]=user.role
            # encoded_jwt = jwt.encode(logininfo, 'secret_key',algorithm='HS256')
            # encoded_jwt = bytes.decode(encoded_jwt)
            data = {}
            data['id'] = user[0].id
            data['user'] = user[0].username
            data['role'] = user[0].role
            data['retoken'] = token
            if user[0].role == 0:
                data['avatar'] = BASE_URL+"/media/avatar/super_manage.jpg"
            elif user[0].role == 1:
                data['avatar'] = BASE_URL+"/media/avatar/school_manage.jpg"
            elif user[0].role == 2:
                data['avatar'] = BASE_URL+"/media/avatar/base_manage.jpg"
            elif user[0].role == 3:
                data['avatar'] = BASE_URL+"/media/avatar/guide_manage.jpg"
            elif user[0].role == 4:
                data['avatar'] = BASE_URL+"/media/avatar/dorm_manage.jpg"
            result = True
            data = data
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})


# 超级管理员对基础设施管理员的账号管理
class SuperBaseView(APIView):

    def get(self, request):
        user_2_all = UserInfo.objects.filter(role=2, is_delete=False)
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
        user_id = request.data.get("user_id", "")
        new_password = request.data.get("new_password", "")
        if user_id == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=2)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        user_id = request.data.get("user_id", "")
        if user_id == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=2)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        time_stamp = int(round(time.time() * 1000))
        change_username = user[0].username+str(time_stamp)
        try:
            user.update(username=change_username, is_delete=True)
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
        user_1_all = UserInfo.objects.filter(role=1, is_delete=False)
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
        user_id = request.data.get("user_id", "")
        new_password = request.data.get("new_password", "")
        if user_id == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=1)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        user_id = request.data.get("user_id", "")
        if user_id == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=1)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        time_stamp = int(round(time.time() * 1000))
        change_username = user[0].username + str(time_stamp)
        try:
            user.update(username=change_username, is_delete=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "学校管理员" + user[0].username + "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

# 所有未绑定宿管的宿舍楼
class UnboundBuildView(APIView):
    def get(self, request):
        unbound_build = DormBuild.objects.filter(manager=None)
        unbound_build_ser = UnboundBuildSerializer(unbound_build, many=True)
        unbound_build_data = unbound_build_ser.data
        result = True
        data = unbound_build_data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


# 超级管理员对宿舍管理员的账号管理
class SuperDormView(APIView):

    def get(self, request):
        user_4_all = UserInfo.objects.filter(role=4, is_delete=False)
        data = []
        for user in user_4_all:
            user_data = UserSerializer(user, many=False)
            user_data = user_data.data
            dorm_manager_id = user_data['id']
            username = user_data['username']
            role = user_data['role']
            builds_infos = DormBuild.objects.filter(manager=user)
            all_build = ""
            for build_info in builds_infos:
                build_name = build_info.buildname
                all_build = build_name
            dorm = {}
            dorm["username"] = username
            dorm["id"] = dorm_manager_id
            dorm["role"] = role
            dorm["all_build"] = all_build
            data.append(dorm)
        result = True
        data = data
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
        build = DormBuild.objects.filter(id=build_id, manager=None)
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
        user_id = request.data.get("user_id", "")
        new_password = request.data.get("new_password", "")
        if user_id == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=4)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        user_id = request.data.get("user_id", "")
        if user_id == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=4)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        time_stamp = int(round(time.time() * 1000))
        change_username = user[0].username + str(time_stamp)
        try:
            user.update(username=change_username, is_delete=True)
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
        user_3_all = UserInfo.objects.filter(role=3, is_delete=False)
        data = []
        for user in user_3_all:
            user_data = UserSerializer(user, many=False)
            user_data = user_data.data
            guide_id = user_data['id']
            username = user_data['username']
            role = user_data['role']
            class_infos = ClassInfo.objects.filter(guide=user)
            all_class = ""
            for class_info in class_infos:
                grade = class_info.grade.grade
                college = class_info.major.college.college_name
                major = class_info.major.major_name
                class_name = class_info.class_name
                per_class = grade+"-"+college+"-"+major+"-"+class_name
                all_class = all_class + per_class + ";"
            guide = {}
            guide["username"] = username
            guide["id"] = guide_id
            guide["role"] = role
            guide["all_class"] = all_class
            data.append(guide)
        result = True
        data = data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

        # user_3_all = UserInfo.objects.filter(role=3)
        # class_list = list()
        # for user in user_3_all:
        #     data = {}
        #     user_data = UserSerializer(user, many=False)
        #     user_data = user_data.data
        #     class_info = ClassInfo.objects.filter(guide=user)
        #     class_data = GlassSerializer(class_info, many=True)
        #     class_data = class_data.data
        #     data["user_data"] = user_data
        #     data["class_data"] = class_data
        #     class_list.append(data)
        # result = True
        # data = class_list
        # error = ""
        # return JsonResponse({"result": result, "data": data, "error": error})

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
        user_id = request.data.get("user_id", "")
        new_password = request.data.get("new_password", "")
        if user_id == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=3)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        user.update(password=secret_new_password)
        result = True
        data = "密码修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        user_id = request.data.get("user_id", "")
        if user_id == '':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=user_id, role=3)
        if not user:
            result = False
            data = ""
            error = "请输入正确用户名密码"
            return JsonResponse({"result": result, "data": data, "error": error})
        time_stamp = int(round(time.time() * 1000))
        change_username = user[0].username + str(time_stamp)
        try:
            user.update(username=change_username, is_delete=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "导员" + user[0].username + "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})



class UserChangePassword(APIView):

    def put(self, request):
        old_password = request.data.get("old_password", "")
        new_password = request.data.get("new_password", "")
        if old_password == "" or new_password == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        user_info = UserInfo.objects.filter(id=user_id)
        if not user_info:
            result = False
            data = ""
            error = "未查询到用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        is_pwd = check_password(old_password, user_info[0].password)
        if not is_pwd:
            result = False
            data = ""
            error = "用户名密码不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        secret_new_password = make_password(new_password, None, 'pbkdf2_sha1')
        try:
            user_info.update(password=secret_new_password)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = True
            data = "修改失败"
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class UnLockView(APIView):

    def post(self, request):
        login_password = request.POST.get("login_password", "")
        if login_password == "":
            result = False
            data = ""
            error = "密码不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        if request.META.get("HTTP_AUTHORIZATION") == None:
            result = False
            data = ""
            error = "token无效"
            return JsonResponse({"result": result, "data": data, "error": error})
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        user_info = UserInfo.objects.filter(id=user_id)
        if not user_info:
            result = False
            data = ""
            error = "未查询到用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        is_pwd = check_password(login_password, user_info[0].password)
        if not is_pwd:
            result = False
            data = ""
            error = "用户名密码不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = ""
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

# 首页数据展示
# 超级管理员：最近登录时间；各账号开通数量；#最近操作记录
# 学校管理员：在校学生总数；毕业生总数；男女比例；各专业人数；总班数；最近登录时间
# 基础设施管理员：最近登录时间；房间数量；入住率；运行闸机数量；其他状态闸机数量；#最近维修记录；
# 导员：最近登录时间；所负责学生总数；#违纪人数；负责班级数量；#违纪排行榜；
# 宿舍管理员：最近登录时间；本楼人数；本楼剩余房间数；入住率；#进出人数时间图；#非正常时间进入人数；
# #非正常时间出人数；#最近非正常时间进入人；#最近非正常时间出门人；#携带进入人；



# {
#     "base":{"last_time":"2019-01-01 20:20:20","last_location":"北京"},
#     "base_count":[{"title":"宿管帐号","number":"1"},{"title":"基础设施管理员","number":"10"},{"title":"学校管理元","number":"5"},{"title":"导员","number":"4"}],
#     "message":[{"title":"通知消息标题"},{"title":"通知消息标题"},{"title":"通知消息标题"},{"title":"通知消息标题"},{"title":"通知消息标题"},{"title":"通知消息标题"}],
#     "echarts":{"type":"pie",
#                "datas":{"dire":["男生人数","女生人数"],
#                         "direses":[
#                                         {value: 453682, name: 'Mon', itemStyle: {normal: {color: '#2d8cf0'}}},
#                                         {value: 879545, name: 'Tues', itemStyle: {normal: {color: '#2d8cf0'}}},
#                                         {value: 2354678, name: 'Wed', itemStyle: {normal: {color: '#2d8cf0'}}},
#                                         {value: 1598403, name: 'Thur', itemStyle: {normal: {color: '#2d8cf0'}}},
#                                         {value: 543250, name: 'Fri', itemStyle: {normal: {color: '#2d8cf0'}}},
#                                         {value: 1305923, name: 'Sat', itemStyle: {normal: {color: '#2d8cf0'}}},
#                                         {value: 1103456, name: 'Sun', itemStyle: {normal: {color: '#2d8cf0'}}}
#                                     ]
#                         }
#                }
#
# }




class ShowIndexView(APIView):
    def get(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            result = False
            data = ""
            error = "无权限"
            return JsonResponse({"result": result, "data": data, "error": error})
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        if a['role'] == 0:
            index = IndexDataView()
            data = {}
            # 最近登录时间；
            last_login = index.last_login(a)
            data['base'] = last_login
            # 各账号开通数量；
            account_number = index.account_number()
            data['base_count'] = account_number
            # 最近操作记录
            last_operation = index.last_operation(a)
            data['message'] = last_operation
            # echarts
            login_times_echarts = index.login_times_echarts()
            data['echarts'] = login_times_echarts
            return JsonResponse(data)
        elif a['role'] == 1:
            index = IndexDataView()
            data = {}
            # 最近登录时间；
            last_login = index.last_login(a)
            data['base'] = last_login
            # 在校学生总数, 毕业生总数, 总班数, 已开通班级数


            return JsonResponse(data)

        elif a['role'] == 2:
                pass
        elif a['role'] == 3:
                pass
        elif a['role'] == 4:
            index = IndexDataView()
            # 最近登录时间；
            last_login = index.last_login(a)
            base_count_todata = []
            b_c_todata = {}
            b_c_todata['title'] = '本楼人数'
            b_c_todata['number'] = index.build_number(a)
            b_c_todata['icon'] = 'pricetags'
            b_c_todata['color'] = '#2d8cf0'
            base_count_todata.append(b_c_todata)
            b_c_todata['title'] = '本楼剩余房间数'
            b_c_todata['number'] = index.remain_number(a)
            b_c_todata['icon'] = 'unlocked'
            b_c_todata['color'] = '#64d572'
            base_count_todata.append(b_c_todata)
            m = index.unusualentryorexit(a)
            b_c_todata['title'] = '本楼非正常时间进入人数'
            b_c_todata['number'] = m[0]
            b_c_todata['icon'] = 'unlocked'
            b_c_todata['color'] = '#64d572'
            base_count_todata.append(b_c_todata)
            b_c_todata['title'] = '本楼非正常时间出门人数'
            b_c_todata['number'] = m[1]
            b_c_todata['icon'] = 'unlocked'
            b_c_todata['color'] = '#64d572'
            base_count_todata.append(b_c_todata)
            message_todata = index.last_operation(a)
            e_type = 'pie'
            todire = ['入住人数','总人数']
            todi = index.build_occupancy_rate(a)
            index_template(last_login,base_count_todata,message_todata,e_type,todire,todi)
        else:
            result = False
            data = ""
            error = "无权限"
            return JsonResponse({"result": result, "data": data, "error": error})


class IndexDataView(APIView):
    """
    首页数据展示
    """

    def last_login(self, a):
        """
        最近登录时间
        param : token
        return:
        """
        user_id = a['user_id']
        # user_id = 2
        user = UserInfo.objects.filter(id=user_id)
        login_data = {}
        if user[0].recent_time == None:
            last_time = "0000-00-00 00:00:00"
            last_location = "北京"
        else:
            last_time = user[0].recent_time
            last_time = str(datetime.datetime.strptime(str(last_time)[:19], "%Y-%m-%d %H:%M:%S"))
            last_location = "北京"
        login_data["last_time"] = last_time
        login_data["last_location"] = last_location
        return login_data


    def account_number(self):
        """
        各账号开通数量
        :param token:
        :return:
        """
        school_admin = UserInfo.objects.filter(role=1, is_delete=False)
        base_admin = UserInfo.objects.filter(role=2, is_delete=False)
        guide_admin = UserInfo.objects.filter(role=3, is_delete=False)
        dorm_admin = UserInfo.objects.filter(role=4, is_delete=False)
        data_list = []
        if school_admin == None:
            data = {}
            school_admin_number = 0
            data["title"] = "学校管理员"
            data["number"] = school_admin_number
            data["icon"] = "person-stalker"
            data["color"] = "#2d8cf0"
            data_list.append(data)
        else:
            data = {}
            school_admin_number = school_admin.count()
            data["title"] = "学校管理员"
            data["number"] = school_admin_number
            data["icon"] = "person-stalker"
            data["color"] = "#2d8cf0"
            data_list.append(data)
        if base_admin == None:
            data = {}
            base_admin_number = 0
            data["title"] = "基础设施管理员"
            data["number"] = base_admin_number
            data["icon"] = "ios-home"
            data["color"] = "#64d572"
            data_list.append(data)
        else:
            data = {}
            base_admin_number = base_admin.count()
            data["title"] = "基础设施管理员"
            data["number"] = base_admin_number
            data["icon"] = "ios-home"
            data["color"] = "#64d572"
            data_list.append(data)
        if guide_admin == None:
            data = {}
            guide_admin_number = 0
            data["title"] = "导员"
            data["number"] = guide_admin_number
            data["icon"] = "bowtie"
            data["color"] = "#ffd572"
            data_list.append(data)
        else:
            data = {}
            guide_admin_number = guide_admin.count()
            data["title"] = "导员"
            data["number"] = guide_admin_number
            data["icon"] = "bowtie"
            data["color"] = "#ffd572"
            data_list.append(data)
        if dorm_admin == None:
            data = {}
            dorm_admin_number = 0
            data["title"] = "宿舍管理员"
            data["number"] = dorm_admin_number
            data["icon"] = "tshirt"
            data["color"] = "#f25e43"
            data_list.append(data)
        else:
            data = {}
            dorm_admin_number = dorm_admin.count()
            data["title"] = "宿舍管理员"
            data["number"] = dorm_admin_number
            data["icon"] = "tshirt"
            data["color"] = "#f25e43"
            data_list.append(data)
        return data_list

    def last_operation(self, a):
        """
        用户最近操作记录
        :param a:
        :return:
        """
        user_id = a['user_id']
        # user_id = 2
        # unread = []
        # hasread = []
        msg_datas = MessageNews.objects.filter(to_user_id=user_id, is_delete=False)
        data = []
        for msg_data in msg_datas:
            msg = {}
            # msg['id'] = msg_data.id
            msg['title'] = msg_data.title
            # msg['time'] = str(datetime.datetime.strptime(str(msg_data.msg_time)[:19], "%Y-%m-%d %H:%M:%S"))
            # if msg_data.is_read:
            #     hasread.append(msg)
            # else:
            #     unread.append(msg)
            data.append(msg)
        # data = {}
        # data['unread'] = unread
        # data['hasread'] = hasread
        return data

    def show_avatar(self):
        """
        头像
        :return:
        """
        data = {}
        data['role_0'] = BASE_URL + "/media/avatar/super_manage.jpg"
        data['role_1'] = BASE_URL + "/media/avatar/school_manage.jpg"
        data['role_2'] = BASE_URL + "/media/avatar/base_manage.jpg"
        data['role_3'] = BASE_URL + "/media/avatar/guide_manage.jpg"
        data['role_4'] = BASE_URL + "/media/avatar/dorm_manage.jpg"
        return data

    def login_times_echarts(self):
        """
        各账号登录次数
        :return:
        """
        users = UserInfo.objects.filter(~Q(role=0), is_delete=False)
        role_legend = []
        value_1 = 0
        value_2 = 0
        value_3 = 0
        value_4 = 0
        for user in users:
            user_role = user.role
            if user_role == 1:
                value_1 += 1
            elif user_role == 2:
                value_2 += 1
            elif user_role == 3:
                value_3 += 1
            elif user_role == 4:
                value_4 += 1
            role_name = user.get_role()
            role_legend.append(role_name)
        role_legend = list(set(role_legend))
        direses_list = []
        for user in role_legend:
            if user == "学校管理员":
                per_user_data = {}
                itemStyle = {}
                normal = {}
                per_user_data['value'] = value_1
                per_user_data['name'] = user
                normal["color"] = "#2d8cf0"
                itemStyle["normal"] = normal
                per_user_data['itemStyle'] = itemStyle
                direses_list.append(per_user_data)
            if user == "基础设施管理员":
                per_user_data = {}
                itemStyle = {}
                normal = {}
                per_user_data['value'] = value_2
                per_user_data['name'] = user
                normal["color"] = "#64d572"
                itemStyle["normal"] = normal
                per_user_data['itemStyle'] = itemStyle
                direses_list.append(per_user_data)
            if user == "导员":
                per_user_data = {}
                itemStyle = {}
                normal = {}
                per_user_data['value'] = value_3
                per_user_data['name'] = user
                normal["color"] = "#ffd572"
                itemStyle["normal"] = normal
                per_user_data['itemStyle'] = itemStyle
                direses_list.append(per_user_data)
            if user == "宿舍管理员":
                per_user_data = {}
                itemStyle = {}
                normal = {}
                per_user_data['value'] = value_4
                per_user_data['name'] = user
                normal["color"] = "#f25e43"
                itemStyle["normal"] = normal
                per_user_data['itemStyle'] = itemStyle
                direses_list.append(per_user_data)
        datas = {}
        datas["dire"] = role_legend
        datas["direses"] = direses_list
        echarts = {}
        echarts["type"] = "bar"
        echarts["datas"] = datas
        return echarts

    def in_school_number(self):
        """
        在校学生总数
        :return:
        """
        student_number = Student.objects.filter(isGraduate=False).count()
        result = True
        data = student_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def graduate_number(self):
        """
        毕业学生总数
        :return:
        """
        student_number = Student.objects.filter(isGraduate=True).count()
        result = True
        data = student_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def male_female_ratio(self):
        """
        男女比例
        :return:
        """
        male_number = Student.objects.filter(sex=0, isGraduate=False)
        female_number = Student.objects.filter(sex=1, isGraduate=False)
        total_number = Student.objects.filter(isGraduate=False)
        if male_number == None:
            male_ratio = 0
            result = True
            data = male_ratio
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        if female_number == None:
            female_ratio = 0
            result = True
            data = female_ratio
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        if total_number == None:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        male_ratio = "%.2f%%" % (float(male_number) / total_number * 100)
        female_ratio = "%.2f%%" % (float(female_number) / total_number * 100)
        data = {}
        data['male_ratio'] = male_ratio
        data['female_ratio'] = female_ratio
        result = True
        data = data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def various_major_number(self):
        """
        各专业人数
        :return:
        """
        major_que = Major.objects.filter(isDelete=False)
        if major_que == None:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        major_list = []
        for major_per in major_que:
            major_info = {}
            major_name = major_per.major_name
            major_per_number = major_per.count()
            major_info['major_name'] = major_name
            major_info['major_per_number'] = major_per_number
            major_list.append(major_info)
        result = True
        data = major_list
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def class_number(self):
        """
        总班级数
        :return:
        """
        class_que = ClassInfo.objects.filter(is_graduation=False)
        if class_que == None:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        class_number = class_que.count()
        result = True
        data = class_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def room_number(self):
        """
        房间数
        :return:
        """
        dorm_room = DormRoom.objects.all()
        if dorm_room == None:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        dorm_room_number = dorm_room.count()
        result = False
        data = dorm_room_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def occupancy_rate(self):
        """
        入住率
        :return:
        """
        room_que = DormRoom.objects.all()
        total_bed_number = 0
        for room in room_que:
            room_bed_number = 0
            if room.room_type == 0:
                room_bed_number += 4
            elif room.room_type == 1:
                room_bed_number += 6
            elif room.room_type == 2:
                room_bed_number += 8
            total_bed_number += room_bed_number
        already_stay_number = BedNumber.objects.exclude(student=None).count()
        # stay_rate = "%.2f%%" % (float(already_stay_number) / total_bed_number * 100)
        data= []
        data.append(already_stay_number)
        data.append(total_bed_number)
        return data

    def gates_machine_number(self):
        """
        运行闸机数量
        :return:
        """
        gates_number = FaceMachine.objects.filter(machine_status=1).count()
        result = True
        data = gates_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def other_machine_number(self):
        """
        其他状态闸机数量
        :return:
        """
        other_number = FaceMachine.objects.exclude(machine_status=1).count()
        result = True
        data = other_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def res_student_num(self, token):
        """
        导员所负责学生总数
        :return:
        """
        user_id = token['user_id']
        total_class = ClassInfo.objects.filter(guide_id=user_id)  # 导员负责的所有班级
        if total_class == None:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        total_number = 0
        for per_class in total_class:
            class_student_number = StudentDetail.objects.filter(class_info=per_class).count()
            total_number += class_student_number
        result = True
        data = total_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def res_class_num(self, token):
        """
        导员负责班级数量
        :param token:
        :return:
        """
        user_id = token['user_id']
        total_class = ClassInfo.objects.filter(guide_id=user_id)
        if total_class == None:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        total_number = total_class.count()
        result = True
        data = total_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def build_number(self, token):
        """
        宿舍管理员本楼人数
        :return:
        """
        user_id = token['user_id']
        build_obj = DormBuild.objects.filter(manager_id=user_id).first()
        if not build_obj:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        all_rooms = build_obj.dormroom_set.all()
        all_room_num = 0
        for room in all_rooms:
            room_student_num = BedNumber.objects.filter(~Q(student=''), room=room).count()
            all_room_num += room_student_num
        result = True
        data = all_room_num
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def remain_number(self, token):
        """
        宿舍管理员本楼剩余房间数
        :return:
        """
        user_id = token['user_id']
        build_obj = DormBuild.objects.filter(manager_id=user_id).first()
        if not build_obj:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        all_rooms = DormRoom.objects.filter(build=build_obj)
        room_number = 0
        for room in all_rooms:
            if BedNumber.objects.filter(~Q(student=""), room=room):
                continue
            else:
                room_number += 1
        result = True
        data = room_number
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def build_occupancy_rate(self, token):
        """
        宿舍管理员本楼入住率
        :return:
        """
        user_id = token['user_id']
        build_obj = DormBuild.objects.filter(manager_id=user_id).first()
        if not build_obj:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        all_rooms = DormRoom.objects.filter(build=build_obj)
        total_bed_number = 0
        for room in all_rooms:
            room_bed_number = 0
            if room.room_type == 0:
                room_bed_number += 4
            elif room.room_type == 1:
                room_bed_number += 6
            elif room.room_type == 2:
                room_bed_number += 8
            total_bed_number += room_bed_number
        already_stay_number = BedNumber.objects.filter(~Q(student=None), room__build=build_obj).count()
        stay_rate = "%.2f%%" % (float(already_stay_number) / total_bed_number * 100)

        data =[]
        d ={}
        d['入住人数']=already_stay_number
        d['总人数']=total_bed_number

        data.append(d)


        return data

    def unusualentryorexit(self,token):
        """
        the count of unusually enter
        :return:
        """
        user_id = token['user_id']
        start_time = datetime.datetime.strptime('00:00:00', '%H:%M:%S')
        end_time = datetime.datetime.strptime('04:00:00', '%H:%M:%S')
        access_datas = AccessRecords.objects.filter(build__manager_id=user_id)
        data = {}
        i = 0
        j = 0
        for access_data in access_datas:
            en_datatime = datetime.datetime.strptime(str(access_data.enter_time)[11:], '%H:%M:%S')
            ex_datatime = datetime.datetime.strptime(str(access_data.entry_time)[11:], '%H:%M:%S')
            if en_datatime > start_time and en_datatime < end_time:
                i = i + 1
            if ex_datatime > start_time and ex_datatime < end_time:
                j = j + 1
        data['enter_count'] = i
        data['entry_count'] = j
        return data


# 通知消息
class MessageNewsView(APIView):

    def get(self, request):
        import time
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        unread = []
        hasread = []
        msg_datas = MessageNews.objects.filter(to_user_id=user_id,is_delete=False)
        for msg_data in msg_datas:
            msg = {}
            msg['id'] = msg_data.id
            msg['title'] = msg_data.title
            msg['time'] = str(datetime.datetime.strptime(str(msg_data.msg_time)[:19], "%Y-%m-%d %H:%M:%S"))
            if msg_data.is_read:
                hasread.append(msg)
            else:
                unread.append(msg)
        data={}
        data['unread'] = unread
        data['hasread'] = hasread
        result = True
        data = data
        error = ""
        print(data )
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        msg_id = request.data.get('msg_id', '')
        msg_data = MessageNews.objects.filter(id=msg_id).update(is_read=True)
        result = True
        data = '已读'
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    # sudo apt-get remove linux-image-4.10.0-28-generic
    def delete(self, request):
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        msg_id = request.data.get('msg_id', '')
        msg_data = MessageNews.objects.filter(id=msg_id, to_user_id=user_id).update(is_delete=True)
        result = True
        data = '删除成功'
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class MessageDetailView(APIView):

    def get(self, request):
        print('##################')
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        msg_id = request.GET.get('msg_id', '')
        print("@@@@@",msg_id)
        msg_data_sql = MessageNews.objects.get(id=msg_id, to_user_id=user_id)
        msg_data = MessageSerializer(msg_data_sql,many=False)
        print(msg_data.data)
        result = True
        data = msg_data.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})






# last_time,base_count_todata,

def index_template(last_time,base_count_todata,message_todata,e_type,todire,todi):
    datas ={}
    base_data={}
    base_data['last_time']=last_time
    base_data['last_location']='北京'
    datas['base']=base_data
    base_count_datas=[]
    for b_c_d in base_count_todata:
        base_count_data={}
        base_count_data['title']=b_c_d.title
        base_count_data['number']=b_c_d.number
        base_count_data['icon']=b_c_d.icon
        base_count_data['color']=b_c_d.color
        base_count_datas.append(base_count_data)
    datas['base_count']=base_count_datas
    message_datas=[]
    for m_d in message_todata:
        message_data={}
        message_data['title']=m_d.title
        message_datas.append(message_datas)
    datas['message']=message_datas
    echarts_data={}
    echarts_data['type']=e_type
    e_datas={}
    dire_data=[]
    for dire in todire:
        dire_data.append(dire)
    e_datas['dire']=dire_data
    direses=[]
    for di in todi:
        direse={}
        direse['value']=di.value
        direse['name']=di.name
        itemStyle={}
        normal={}
        normal['color']='red'
        itemStyle['normal']=normal
        direse['itemStyle']=itemStyle
        direses.append(direse)
    e_datas['direses']=direses
    echarts_data['datas']=e_datas
    datas['echarts1']=echarts_data
    return datas
    # datas['echarts2']=



# datas ={}
# base_data={}
# base_data['last_time']=last_time
# base_data['last_location']='北京'
# datas['base']=base_data
# base_count_datas=[]
# base_count_data={}
# base_count_data['title']=
# base_count_data['number']=
# base_count_data['number']=
# base_count_datas.append(base_count_data)
# datas['base_count']=base_count_datas
# message_datas=[]
# message_data={}
# message_data['title']=
# message_datas.append(message_datas)
# datas['message']=message_datas
# echarts_data={}
# echarts_data['type']=
# e_datas={}
# dire_data=[]
# dire_data.append('')
# e_datas['dire']=
# direses=[]
# direse={}
# direse['value']=
# direse['name']=
# itemStyle={}
# normal={}
# normal['color']=
# itemStyle['normal']=normal
# direse['itemStyle']=itemStyle
# direses.append(direse)
# e_datas['direses']=direses
# echarts_data['datas']=e_datas
# datas['echarts1']=echarts_data
# datas['echarts2']=
