from django.shortcuts import render
# restful API
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions

#django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse,request

# selfproject
from .serializers import *
from .permissions import *
from .models import *

# base
import logging
import json
import datetime
import time


logger = logging.getLogger('sourceDns.webdns.views')
# Create your views here.

# build edit
class BuildingEdit(APIView):
    permission_classes = (
        IsConnAdmin,
    )

    def get(self, request):
        build = DormBuild.objects.filter(is_delete=False)
        builddata = BuildSerializer(build, many=True)
        result = True
        data = builddata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        buildname = request.POST.get("buildname", "")
        if buildname == "":
            result = False
            data = ""
            error = "楼名不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldbuild = DormBuild.objects.filter(buildname=buildname)
        if oldbuild:
            result = False
            data = ""
            error = "楼名不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        else:
            try:
                DormBuild.objects.create(buildname=buildname)
            except ObjectDoesNotExist as e:
                logger.error(e)
            result = True
            data = "添加成功"
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        buildid = request.data.get("buildid", '')
        if buildid == "":
            result = False
            data = ""
            error = "id不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldbuild = DormBuild.objects.filter(id=buildid)
        if not oldbuild:
            result = False
            data = ""
            error = "未找到宿舍楼"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldbuild.update(is_delete=True)
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        buildid = request.data.get("buildid", "")
        buildname = request.data.get("buildname", "")
        if buildid == "" or buildname == "":
            result = False
            data = ""
            error = "id,楼名不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            build = DormBuild.objects.get(id=buildid)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未找到楼信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        build.buildname = buildname
        build.save()
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class RoomEdit(APIView):
    # permission_classes = (
    #     IsConnAdmin,
    # )

    def get(self, request):
        buildid = request.GET.get("buildid", "")
        if buildid == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            build = DormBuild.objects.get(id=buildid)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "id不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        rooms = DormRoom.objects.filter(build_id=buildid)
        roomsdata = BedNumberSerializer(rooms, many=True)
        result = True
        data = roomsdata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        roomno = request.POST.get("roomno", "")
        buildid = request.POST.get("buildid", "")
        roomtype = request.POST.get("roomtype", "")
        if roomno == "" or buildid == "" or roomtype == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            build = DormBuild.objects.get(id=buildid)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "宿舍楼id不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            DormRoom.objects.create(build=build, room_id=roomno,room_type=roomtype)
        except ObjectDoesNotExist as e:
            logger.error(e)
        result = True
        data = "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        roomid = request.data.get("roomid", "")
        if roomid == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            old_room = DormRoom.objects.filter(id=roomid)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = True
            data = ""
            error = "未找到该宿舍"
            return JsonResponse({"result": result, "data": data, "error": error})
        old_room.delete()
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        pass


class BedEdit(APIView):
    def post(self, request):
        build_id = request.POST.get("buildid", "")
        room_id = request.POST.get("roomid", "")
        bed_num = request.POST.get("bed_num", "")
        if build_id == "" or room_id == "" or bed_num == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        old_room = DormRoom.objects.filter(build_id=build_id, id=room_id)
        if not old_room:
            result = False
            data = ""
            error = "未找到宿舍"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            BedNumber.objects.create(room=old_room, bed_num=bed_num)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "参数有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class EnterRecordView(APIView):
    def post(self, request):
        student_code = request.POST.get("student_code", "")
        enter_time_str = request.POST.get("enter_time", "")
        # enter_time 是一个日期格式的字符串，形式示例：2016-05-09 21:09:30
        if student_code == "" or enter_time_str == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.get(studentid=student_code)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未查询到该学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            enter_time = datetime.datetime.strptime(enter_time_str, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            logger.error(e)
            result = False
            data = ""
            error = "参数格式有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        time_str = time.time.strptime(enter_time_str[11:], "%H:%M:%S")
        print(time_str)
        latest_time = "23:00:00"
        try:
            AccessRecords.objects.create(student=student, enter_time=enter_time)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "进入登记失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = ""
        error = "进入登记成功"
        return JsonResponse({"result": result, "data": data, "error": error})


class EntryRecordView(APIView):
    def post(self, request):
        student_code = request.POST.get("student_code", "")
        entry_time = request.POST.get("entry_time", "")
        if student_code == "" or entry_time == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.get(studentid=student_code)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未查询到该学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            AccessRecords.objects.create(student=student, enter_time=entry_time)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "出入登记失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = ""
        error = "出入登记成功"
        return JsonResponse({"result": result, "data": data, "error": error})


class TemportaryPersonEnter(APIView):

    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        name = request.POST.get("name", "")
        mobile = request.POST.get("mobile", "")
        relation = request.POST.get("relation", "")
        enter_time = request.POST.get("enter_time", "")
        if student_code == "" or student_name == "" or name == "" or mobile == "" or relation == "" or enter_time == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.get(studentid=student_code, name=student_name)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "为查询到学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            TemporaryPersonRecords.objects.create(student=student, name=name, mobile=mobile, relation=relation, enter_time=enter_time, is_carry=False)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "登记临时人员进入失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "登记临时人员进入成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class TemportaryPersonEntry(APIView):

    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        name = request.POST.get("name", "")
        entry_time = request.POST.get("entry_time", "")
        if student_code == "" or student_name == "" or name == "" or entry_time == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.get(studentid=student_code, name=student_name)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "为查询到学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            tem_person = TemporaryPersonRecords.objects.filter(student_id=student.id, name=name, is_carry=False)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未查询到临时人员进入记录"
            return JsonResponse({"result": result, "data": data, "error": error})
        tem_person.update(entry_time=entry_time)
        result = True
        data = "登记临时人员出入成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class ExportAccessView(APIView):

    def get(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        if student_code == "" or student_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        student = Student.objects.filter(studentid=student_code, name=student_name)
        if not student:
            result = False
            data = ""
            error = "未查询到学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        access_record = AccessRecords.objects.filter(student=student)
        if not access_record:
            result = False
            data = ""
            error = "未查询到学生进出记录"
            return JsonResponse({"result": result, "data": data, "error": error})
        access_data = AccessRecordSerializer(access_record, many=True)
        access_data = access_data.data
        result = True
        data = access_data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class LongTimeEnter(APIView):
    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        if student_code == "" or student_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        student = Student.objects.filter(studentid=student_code, name=student_name)
        if not student:
            result = False
            data = ""
            error = "请输入正确学生学号姓名"
            return JsonResponse({"result": result, "data": data, "error": error})
        student_access = AccessRecords.objects.filter(student=student)
        if not student_access:
            result = False
            data = ""
            error = "未查询到该同学的出入记录"
            return JsonResponse({"result": result, "data": data, "error": error})
        enter_time = student_access[0].enter_time
        now_time = datetime.datetime.now()
        differ_time = now_time-enter_time
        differ_time_days = differ_time.days
        if differ_time_days >= 2:
            result = True
            data = ""
            error = "该同学已超过2天未进入宿舍"
            return JsonResponse({"result": result, "data": data, "error": error})
        else:
            result = True
            data = ""
            error = "该同学正常出入宿舍"
            return JsonResponse({"result": result, "data": data, "error": error})



class LongTimeEntry(APIView):
    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        if student_code == "" or student_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        student = Student.objects.filter(studentid=student_code, name=student_name)
        if not student:
            result = False
            data = ""
            error = "请输入正确学生学号姓名"
            return JsonResponse({"result": result, "data": data, "error": error})
        student_access = AccessRecords.objects.filter(student=student)
        if not student_access:
            result = False
            data = ""
            error = "未查询到该同学的出入记录"
            return JsonResponse({"result": result, "data": data, "error": error})
        entry_time = student_access[0].entry_time
        now_time = datetime.datetime.now()
        differ_time = now_time-entry_time
        differ_time_days = differ_time.days
        if differ_time_days >= 2:
            result = True
            data = ""
            error = "该同学已超过2天未出入宿舍"
            return JsonResponse({"result": result, "data": data, "error": error})
        else:
            result = True
            data = ""
            error = "该同学正常出入宿舍"
            return JsonResponse({"result": result, "data": data, "error": error})


class CarryPersonEnter(APIView):

    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        name = request.POST.get("name", "")
        mobile = request.POST.get("mobile", "")
        relation = request.POST.get("relation", "")
        enter_time = request.POST.get("enter_time", "")
        if student_code == "" or student_name == "" or name == "" or mobile == "" or relation == "" or enter_time == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.get(studentid=student_code, name=student_name)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "为查询到学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            TemporaryPersonRecords.objects.create(student=student, name=name, mobile=mobile, relation=relation, enter_time=enter_time, is_carry=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "登记临时人员进入失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "登记临时人员进入成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class CarryPersonEntry(APIView):
    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        name = request.POST.get("name", "")
        entry_time = request.POST.get("entry_time", "")
        if student_code == "" or student_name == "" or name == "" or entry_time == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.get(studentid=student_code, name=student_name)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "为查询到学生信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            tem_person = TemporaryPersonRecords.objects.filter(student_id=student.id, name=name, is_carry=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未查询到临时人员进入记录"
            return JsonResponse({"result": result, "data": data, "error": error})
        tem_person.update(entry_time=entry_time)
        result = True
        data = "登记临时人员出入成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class EnterTimeLate(APIView):

    def post(self, request):
        pass









