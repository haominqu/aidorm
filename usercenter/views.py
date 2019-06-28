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
from dormitory.serializers import BuildSerializer, UnboundBuildSerializer
from .serializers import *
from .permissions import *
from .models import *
from aidorm.settings import BASE_URL

# base
import logging
import json
import jwt
import datetime


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
        try:
            user.update(is_delete=True)
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
        try:
            user.update(is_delete=True)
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
        try:
            user.update(is_delete=True)
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
        try:
            user.update(is_delete=True)
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
# 超级管理员：最近登录时间；各账号开通数量；最近操作记录
# 学校管理员：在校学生总数；毕业生总数；男女比例；各专业人数；总班数；最近登录时间
# 基础设施管理员：最近登录时间；房间数量；入住率；运行闸机数量；其他状态闸机数量；最近维修记录；
# 导员：最近登录时间；所负责学生总数；违纪人数；负责班级数量；违纪排行榜；
# 宿舍管理员：最近登录时间；本楼人数；本楼剩余房间数；入住率；进出人数时间图；非正常时间进入人数；
# 非正常时间出人数；最近非正常时间进入人；最近非正常时间出门人；携带进入人；


class IndexLastLogin(APIView):

    def get(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            result = False
            data = ""
            error = "token无效"
            return JsonResponse({"result": result, "data": data, "error": error})
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        user = UserInfo.objects.filter(id=user_id)
        if not user:
            result = False
            data = ""
            error = "未查询到用户"
            return JsonResponse({"result": result, "data": data, "error": error})
        if user[0].recent_time == None:
            pass
        last_time = user[0].recent_time
        result = True
        data = last_time
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


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



