# restful API
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions

# django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# selfproject
from .serializers import *
from .permissions import *
from .models import *

# base
import logging
import json

# Create your views here.
class CollegeEdit(APIView):
    # permission_classes = (
    #     IsCollegeAdmin,
    # )

    def get(self, request):
        college = College.objects.all()
        collegedata = CollegeSerializer(college, many=True)
        result = True
        data = collegedata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        """method of adding college"""
        collid = request.POST.get("collid", '')
        collname = request.POST.get("collname", '')
        if collid == "" or collname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldcoll = College.objects.filter(college_id=collid, college_name=collname)
        if oldcoll:
            result = False
            data = ""
            error = "信息不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            College.objects.create(college_id=collid, college_name=collname)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        result = True
        data = ""
        error = "添加成功"
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        """method of deleting college"""
        collid = request.POST.get("collid", '')
        collname = request.POST.get("collname", '')
        if collid == "" or collname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            oldcoll = College.objects.filter(college_id=collid, college_name=collname)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "未找到"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldcoll.update(isDelete=True)
        result = True
        data = ""
        error = "删除成功"
        return JsonResponse({"result": result, "data": data, "error": error})

    def patch(self, request):
        pass


class MajorEdit(APIView):
    def get(self, requset):
        major = Major.objects.all()
        majordata = MajorSerializer(major, many=True)
        result = True
        data = majordata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        collid = request.POST.get("collid", '')
        majorid = request.POST.get("majorid", '')
        majorname = request.POST.get("majorname", '')
        if collid == "" or majorid == "" or majorname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            college = College.objects.get(id=collid)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "未找到院系信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        Major.objects.create(college=college, major_id=majorid, major_name=majorname)
        result = True
        data = ""
        error = "添加成功"
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        """method of deleting major"""
        majorid = request.POST.get("majorid", '')
        majorname = request.POST.get("majorname", '')
        if majorid == "" or majorname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            oldmajor = Major.objects.filter(major_id=majorid, major_name=majorname)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "未找到"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor.update(isDelete=True)
        result = True
        data = ""
        error = "删除成功"
        return JsonResponse({"result": result, "data": data, "error": error})

    def patch(self, requset):
        pass

class GradeEdit(APIView):
    def get(self, request):
        pass

    def post(self, request):
        grade = request.POST.get("grade", "")
        if grade == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            Grade.objects.create(grade=grade)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        result = True
        data = ""
        error = "添加成功"
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        pass

    def patch(self, request):
        pass

