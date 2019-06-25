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
from student.models import *

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
        """
        默认获取全部专业列表； 院系、专业二级联动
        param request: collid： 院系id
        return:
        """
        collid = request.GET.get("collid", "")
        if collid == "":
            major = Major.objects.filter(isDelete=False)
        else:
            college = College.objects.filter(id=collid)
            major = Major.objects.filter(college=college, isDelete=False)
        majordata = MajorSerializer(major, many=True)
        result = True
        data = majordata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        """
        新建一个已创建院系的专业
        param request: collid:院系id; majorcode:专业代码; majorname:专业名称
        return:
        """
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
    permission_classes = (
        IsSchoolAdmin,
    )


    def get(self, request):
        """
        默认获取全部班级信息列表； 可按年级、院系筛选班级
        param request: 院系id 年级id
        return: id, 班级名称, 年级, 院系, 专业, 导员, 总人数, 是否毕业
        """
        college_id = request.GET.get("college_id", "")
        grade_id = request.GET.get("grade_id", "")
        if college_id == "" and grade_id == "":
            all_class = ClassInfo.objects.all()
        elif college_id == "" and grade_id != "":
            all_class = ClassInfo.objects.filter(grade_id=grade_id)
        elif college_id != "" and grade_id == "":
            all_class = ClassInfo.objects.filter(major__college_id=college_id)
        elif college_id != "" and grade_id != "":
            all_class = ClassInfo.objects.filter(major__college_id=college_id, grade_id=grade_id)
        data = []
        for per_class in all_class:
            per_class_ser = GlassSerializer(per_class, many=False)
            per_class_data = per_class_ser.data
            total_number = per_class.studentdetail_set.all().count()
            per_class_data["total_number"] = total_number
            data.append(per_class_data)
        result = True
        data = data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


    def post(self, request):
        """
        创建班级并为班级绑定导员
        :param request:
        :return:
        """
        college_id = request.POST.get("college_id", "")
        major_id = request.POST.get("major_id", "")
        grade_id = request.POST.get("grade_id", "")
        class_name = request.POST.get("class_name", "")
        guide_id = request.POST.get("guide_id", "")
        if college_id == "" or major_id == "" or grade_id == "" or class_name == "" or guide_id == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        major = Major.objects.filter(id=major_id, college_id=college_id)
        if not major:
            result = False
            data = ""
            error = "请输入正确院系专业"
            return JsonResponse({"result": result, "data": data, "error": error})
        grade = Grade.objects.filter(id=grade_id)
        if not grade:
            result = False
            data = ""
            error = "请输入正确年级"
            return JsonResponse({"result": result, "data": data, "error": error})
        user = UserInfo.objects.filter(id=guide_id, is_delete=False)
        if not user:
            result = False
            data = ""
            error = "请输入正确导员"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            new_class = ClassInfo.objects.create(major=major[0], grade=grade[0], class_name=class_name, guide=user[0])
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "班级添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            class_code = major[0].college.college_id + major[0].major_id + str(new_class.id)
        except Exception as e:
            logger.error(e)
            new_class.delete()
            result = False
            data = ""
            error = "班级添加失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        new_class = ClassInfo.objects.filter(id=new_class.id)
        new_class.update(class_code=class_code)
        result = True
        data = "成功添加班级并绑定导员"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        """
        修改班级名称，修改班级导员
        :param request:
        :return:
        """
        class_id = request.data.get("class_id", "")
        class_name = request.data.get("class_name", "")
        guide_id = request.data.get("guide_id", "")
        if class_id == "":
            result = False
            data = ""
            error = "班级不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        class_one = ClassInfo.objects.filter(id=class_id)
        if not class_one:
            result = False
            data = ""
            error = "id有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        if class_name != "" and guide_id == "":
            class_one.update(class_name=class_name)
        elif guide_id != "" and class_name == "":
            class_one.update(guide_id=guide_id)
        elif class_name != "" and guide_id != "":
            class_one.update(class_name=class_name, guide_id=guide_id)
        elif class_name == "" and guide_id == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        """
        如果班级信息误填，将其删除；若班级里有学生，不允许删除
        :param request:
        :return:
        """
        class_id = request.data.get("class_id", "")
        if class_id == "":
            result = False
            data = ""
            error = "班级不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        class_graduation = ClassInfo.objects.filter(id=class_id)
        if not class_graduation:
            result = False
            data = ""
            error = "id有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        students = StudentDetail.objects.filter(class_info=class_graduation)
        if students:
            result = False
            data = ""
            error = "该班级有学生不允许删除"
            return JsonResponse({"result": result, "data": data, "error": error})
        class_graduation.delete()
        result = True
        data = ""
        error = "删除成功"
        return JsonResponse({"result": result, "data": data, "error": error})


class AlreadyGraduation(APIView):
    permission_classes = (
        IsSchoolAdmin,
    )

    def delete(self, request):
        """
        如果该班级已毕业, 将其状态设定为毕业
        :param request:
        :return:
        """
        class_id = request.data.get("class_id", "")
        if class_id == "":
            result = False
            data = ""
            error = "班级不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        class_graduation = ClassInfo.objects.filter(id=class_id)
        if not class_graduation:
            result = False
            data = ""
            error = "id有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            class_graduation.update(is_graduation=True)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "已毕业"
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


class CollectFace(APIView):
    def get(self, request):
        return render(request, 'collect_face.html')


class BatchFace(APIView):
    def get(self, request):
        return render(request, 'batch_face.html')

