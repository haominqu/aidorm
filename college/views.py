# restful API
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions

# django
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction

# selfproject
from .serializers import *
from .permissions import *
from .models import *

# base
import logging
import json
import xlrd


logger = logging.getLogger('sourceDns.webdns.views')

# Create your views here.
class CollegeEdit(APIView):
    # permission_classes = (
    #     IsSchoolAdmin,
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
            return JsonResponse({"result":  result, "data": data, "error": error})
        try:
            College.objects.create(college_id=collcode, college_name=collname)
        except ObjectDoesNotExist as e:
            logger.error(e)
        result = True
        data = "添加成功"
        error = ""
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
            logger.error(e)
            result = False
            data = ""
            error = "未找到院系信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldcoll.update(isDelete=True)
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        collid = request.data.get("collid", '')
        collcode = request.data.get("collcode", '')
        collname = request.data.get("collname", '')
        if collid == "" or collcode == "" or collname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            oldcoll = College.objects.filter(id=collid, isDelete=False)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未找到院系信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldcoll.update(college_id=collcode, college_name=collname)
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class MajorEdit(APIView):
    # permission_classes = (
    #     IsSchoolAdmin,
    # )

    def get(self, request):
        collid = request.GET.get("collid", "")
        college = College.objects.filter(id=collid)
        major = Major.objects.filter(college=college, isDelete=False)
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
            logger.error(e)
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
        if majorid == "":
            result = False
            data = ""
            error = "id不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
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
        majorid = request.data.get("majorid", '')
        majorcode = request.data.get("majorcode", '')
        majorname = request.data.get("majorname", '')
        if majorid == "" or majorcode == "" or majorname == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor = Major.objects.filter(id=majorid)
        if not oldmajor:
            result = False
            data = ""
            error = "未找到专业信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        oldmajor.update(major_id=majorcode, major_name=majorname)
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class GradeEdit(APIView):
    # permission_classes = (
    #     IsSchoolAdmin,
    # )

    def get(self, request):
        major = Grade.objects.all()
        gradedata = GradeSerializer(major, many=True)
        result = True
        data = gradedata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

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
            logger.error(e)
        result = True
        data = "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        grade_id = request.data.get('gradeid', "")
        if grade_id == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            Grade.objects.filter(id=grade_id).delete()
        except ObjectDoesNotExist as e:
            logger.error(e)
        result = True
        data = "删除成功"
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



class ClassInfoView(APIView):
    def post(self, request):
        major_code = request.POST.get("major_code", "")
        grade_id = request.POST.get("grade_id", "")
        class_name = request.POST.get("class_name", "")
        guide_id = request.POST.get("guide_id", "")
        guide_name = request.POST.get("guide_name", "")
        if major_code == "" or grade_id == "" or class_name == "" or guide_id == "" or guide_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        major = Major.objects.filter(major_id=major_code)
        if not major:
            result = False
            data = ""
            error = "请输入正确专业代码"
            return JsonResponse({"result": result, "data": data, "error": error})
        grade = Grade.objects.filter(id=grade_id)
        if not grade:
            result = False
            data = ""
            error = "请输入正确年级"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=guide_id, username=guide_name)
        if not user:
            result = False
            data = ""
            error = "请输入正确导员"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            ClassInfo.objects.create(major=major[0], grade=grade[0], class_name=class_name, guide=user[0])
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "班级添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "成功添加班级并绑定导员"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


# from .rexcel import ReadExcel
#
# class SaveData(APIView):
#     def get(self, request):
#         ReadExcel()
#         return True


class BatchInsert(APIView):
    def post(self, request):
        f = request.FILES['my_file']
        type_excel = f.name.split('.')[1]
        if 'xls' == type_excel:
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            nrows = table.nrows
            try:
                with transaction.atomic():
                    for i in range(1, nrows):
                        # if 4 == i:
                        #     i/0
                        rowValues = table.row_values(i)  # 一行的数据
                        print(rowValues)
                        # good = models.GoodsManage.objects.get(international_code=rowValues[0])
                        # models.SupplierGoodsManage.objects.create(goods=good, sale_price=rowValues[1],
                        #                                           sale_min_count=rowValues[2])
            except Exception as e:
                return JsonResponse({'msg': '出现错误....'})
            return JsonResponse({'msg': 'ok'})
        return JsonResponse({'msg': '上传文件格式不是xlsx'})


class Index(APIView):
    def get(self, request):
        return render(request, 'index.html')




