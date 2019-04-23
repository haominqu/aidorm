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

# Create your views here.

# build edit
class BuildingEdit(APIView):
    # permission_classes = (
    #     IsCollegeAdmin,
    # )

    def get(self, request):
        build = DormBuild.objects.all()
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
                logging.warning(e)
            result = True
            data = "添加成功"
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        pass

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
            logging.warning(e)
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
    #     IsCollegeAdmin,
    # )

    def get(self, request):
        room = DormRoom.objects.all()
        roomdata = RoomSerializer(room, many=True)
        result = True
        data = roomdata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        roomno = request.POST.get("roomno", "")
        buildid = request.POST.get("buildid", "")
        roomtype = request.POST.get("roomtype", "")
        overnum = request.POST.get("overnum", "")
        overbed = request.POST.get("overbed", "")
        picture = request.FILES.get('picture', "")
        dormhead = 0
        isFull = False
        build = DormBuild.objects.filter(id=buildid)
        if roomno=="" or buildid=="" or roomtype=="" or overnum=="" or overbed=="" or picture=="":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            DormRoom.objects.create(build=build[0],room_id=roomno,room_type=roomtype,over_num=overnum,over_bed=overbed,picture=picture,dorm_head=dormhead,isFull=isFull)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        result = True
        data = "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        pass

    def patch(self, request):
        pass



