# restful API
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions

# django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db.models import Q

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
        college = College.objects.filter(isDelete=False)
        collegedata = CollegeSerializer(college, many=True)
        result = True
        data = collegedata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        """method of adding college"""
        collcode = request.POST.get("collcode", '')
        collname = request.POST.get("collname", '')
        if collcode == "" or collname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldcoll = College.objects.filter(Q(college_id=collcode) | Q(college_name=collname))
        if oldcoll:
            result = False
            data = ""
            error = "信息不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            College.objects.create(college_id=collcode, college_name=collname)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        result = True
        data = ""
        error = "添加成功"
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        """method of deleting college"""
        collid = request.data.get("collid", '')
        if collid == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            oldcoll = College.objects.filter(id=collid)
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

    def put(self, request):
        collid = request.data.get("collid", '')
        collcode = request.data.get("collcode", '')
        collname = request.data.get("collname", '')
        if collid == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            oldcoll = College.objects.filter(id=collid, isDelete=False)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "未找到"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldcoll.update(college_id=collcode, college_name=collname)
        result = True
        data = ""
        error = "修改成功"
        return JsonResponse({"result": result, "data": data, "error": error})


class MajorEdit(APIView):
    def get(self, request):
        major = Major.objects.filter(isDelete=False)
        majordata = MajorSerializer(major, many=True)
        result = True
        data = majordata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        collid = request.POST.get("collid", '')
        majorcode = request.POST.get("majorcode", '')
        majorname = request.POST.get("majorname", '')
        if collid == "" or majorcode == "" or majorname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            college = College.objects.get(id=collid, isDelete=False)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "未找到院系信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor = Major.objects.filter(Q(major_id=majorcode) | Q(major_name=majorname))
        if oldmajor:
            result = False
            data = ""
            error = "信息不能重复"
            return JsonResponse({"result": result, "data": data, "error": error})
        Major.objects.create(college=college, major_id=majorcode, major_name=majorname)
        result = True
        data = "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        """method of deleting major"""
        majorid = request.data.get("majorid", '')
        oldmajor = Major.objects.filter(id=majorid)
        if not oldmajor:
            result = False
            data = ""
            error = "未找到专业信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor.update(isDelete=True)
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        collid = request.data.get("collid", '')
        majorid = request.data.get("majorid", '')
        majorcode = request.data.get("majorcode", '')
        majorname = request.data.get("majorname", '')
        if collid == "" or majorid == "" or majorcode == "" or majorname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            college = College.objects.get(id=collid, isDelete=False)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "未找到院系信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor = Major.objects.filter(id=majorid)
        if not oldmajor:
            result = False
            data = ""
            error = "未找到专业信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor.update(college=college, major_id=majorcode, major_name=majorname)
        result = True
        data = ""
        error = "修改成功"
        return JsonResponse({"result": result, "data": data, "error": error})


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
        grade = Grade.objects.filter(grade=grade)
        gradedata = GradeSerializer(grade, many=True)
        result = True
        data = gradedata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        grade_id = request.data.get('gradeid', "")
        grade_name = request.data.get('grade', "")
        if grade_id == "" or grade_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        grade = Grade.objects.filter(id=grade_id)
        if not grade:
            result = False
            data = ""
            error = "未找到年级信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        grade.update(grade=grade_name)
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})







