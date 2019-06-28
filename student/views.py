# restful API
import shutil

from rest_framework.views import APIView

#django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import HttpResponse
from django.conf import settings

# selfproject
from rest_framework_jwt.authentication import jwt_decode_handler

from .serializers import *
from .models import *
from college.models import Major
from dormitory.models import *
from dormitory.serializers import *

# base
import logging
import xlrd
import xlwt
import io
import zipfile
import datetime
import time
import os

# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')


class UploadImageTest(APIView):

    def post(self, request):
        if request.META.get("HTTP_AUTHORIZATION") == None:
            result = False
            data = ""
            error = "token无效"
            return JsonResponse({"result": result, "data": data, "error": error})
        token = request.META.get("HTTP_AUTHORIZATION").split(' ')
        a = jwt_decode_handler(token[2])
        user_id = a['user_id']
        face_picture = request.FILES.get('face_picture', '')
        file_type = face_picture.name.split('.')[1]
        time_stamp = int(round(time.time() * 1000))
        file_name = str(user_id) + str(time_stamp) + '.' + file_type
        f = open(os.path.join(settings.BASE_DIR, 'media', 'tempory', file_name), 'wb')
        for chunk in face_picture.chunks():
            f.write(chunk)
        f.close()
        file_path = settings.BASE_URL+"/media/tempory/"+file_name
        result = True
        data = file_path
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


# student edit
class StudentEdit(APIView):

    def get(self, request):
        """
        获取班里的学生信息
        :param request:class_id： 班级id
        :return:
        """
        print(request.path_info)
        class_id = request.GET.get('class_id', '')
        if class_id == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student_detail = StudentDetail.objects.filter(class_info_id=class_id)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        data = {}
        class_infos = ClassInfo.objects.filter(id=class_id)
        data['class_total_name'] = class_infos[0].grade.grade+"-"+class_infos[0].major.college.college_name+"-"+class_infos[0].major.major_name+"-"+class_infos[0].class_name
        student_list = []
        for student in student_detail:
            student_info = {}
            student_info['id'] = student.student.id
            student_info['student_code'] = student.student.studentid
            student_info['student_name'] = student.student.name
            student_info['student_sex'] = student.student.get_sex()
            student_info['student_phone'] = student.student.phone
            student_info['student_liaisons'] = student.liaisons
            student_info['liaisons_mobile'] = student.liaisons_mobile
            student_info['remarks'] = student.st_others
            student_list.append(student_info)
        data['student_infos'] = student_list
        result = True
        data = data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        """
        添加学生
        :param request:
        :return:
        """
        student_code = request.POST.get('student_code', '')
        student_name = request.POST.get('student_name', '')
        gender = request.POST.get('gender', '')
        phone = request.POST.get('phone', '')
        face_picture = request.POST.get('face_picture', '')
        liaisons = request.POST.get('liaisons', '')
        liaisons_mobile = request.POST.get('liaisons_mobile', '')
        st_others = request.POST.get('remarks', '')
        class_id = request.POST.get('class_id', '')
        if student_code=='' or student_name=='' or gender=='' or phone=='' or face_picture == '' or liaisons=='' or liaisons_mobile=='' or class_id=='':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        class_info = ClassInfo.objects.filter(id=class_id)
        if not class_info:
            result = False
            data = ""
            error = "请输入正确班级信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        major = class_info[0].major
        grade = class_info[0].grade

        face_file_name = face_picture.split('/')[-1]
        fixed_file_path = "/media/fixed_face/"
        tempory_file_path = "/media/tempory/"
        abs_path = os.getcwd()
        for file in os.listdir(abs_path+tempory_file_path):
            if file != face_file_name:
                continue
            else:
                shutil.copy(os.path.join(abs_path+tempory_file_path, file), os.path.join(abs_path+fixed_file_path, file))
                os.remove(os.path.join(abs_path+tempory_file_path, face_file_name))
        try:
            new_student = Student.objects.create(studentid=student_code, name=student_name, sex=gender, phone=phone, face=face_file_name)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "添加学生失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            StudentDetail.objects.create(liaisons=liaisons, liaisons_mobile=liaisons_mobile, student=new_student, major=major, grade=grade, class_info=class_info[0], st_others=st_others)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            new_student.delete()
            result = False
            data = ""
            error = "添加学生失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "添加学生成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        student_id = request.data.get('student_id', '')
        if student_id == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.filter(id=student_id)
            student.delete()
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "删除失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "删除成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def put(self, request):
        student_id = request.data.get('student_id', '')
        new_mobile = request.data.get('new_mobile', '')
        liaisons = request.data.get('liaisons', '')
        liaisons_mobile = request.data.get('liaisons_mobile', '')
        if student_id == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        student = Student.objects.filter(id=student_id)
        if not student:
            result = False
            data = ""
            error = "请输入正确学生"
            return JsonResponse({"result": result, "data": data, "error": error})
        if new_mobile:
            student.update(phone=new_mobile)
        student_detail = StudentDetail.objects.filter(student_id=student[0].id)
        if not student_detail:
            result = False
            data = ""
            error = ""
            return JsonResponse({"result": result, "data": data, "error": error})
        if liaisons:
            student_detail.update(liaisons=liaisons)
        if liaisons_mobile:
            student_detail.update(liaisons_mobile=liaisons_mobile)
        result = True
        data = ""
        error = "修改成功"
        return JsonResponse({"result": result, "data": data, "error": error})


class BatchCreateView(APIView):
    def post(self, request):
        file_excel = request.FILES.get("student_excel", "")
        file_zip = request.FILES.get("face_zip", "")
        excel_type = file_excel.name.split('.')[1]
        zip_type = file_zip.name.split('.')[1]
        zip_name = file_zip.name.split('.')[0]
        if excel_type != 'xls' or zip_type != 'zip':
            result = False
            data = ""
            error = "上传文件格式不符合格式"
            return JsonResponse({"result": result, "data": data, "error": error})
        wb = xlrd.open_workbook(filename=None, file_contents=file_excel.read())
        table = wb.sheets()[0]
        nrows = table.nrows
        student_base_list = list()
        student_detail_list = list()
        student_detail_info = list()
        students_codes = list()
        with transaction.atomic():
            for i in range(1, nrows):
                rowValues = table.row_values(i)  # 一行的数据
                students_codes.append(rowValues[0])
                if rowValues[2] == u'男':
                    rowValues[2] = 0
                elif rowValues[2] == u'女':
                    rowValues[2] = 1
                else:
                    rowValues[2] = rowValues[2]
                student_base_list.append(Student(studentid=str(int(rowValues[0])), name=rowValues[1], sex=rowValues[2], phone=str(int(rowValues[3]))))
                student_detail = {}
                student_detail['student_code'] = str(int(rowValues[0]))
                student_detail['name'] = rowValues[1]
                student_detail['liaisons'] = rowValues[4]
                student_detail['liaisons_mobile'] = str(int(rowValues[5]))
                student_detail['major_code'] = str(int(rowValues[6]))
                student_detail['major'] = rowValues[7]
                student_detail['grade'] = rowValues[8]
                student_detail['class_info'] = rowValues[9]
                student_detail_info.append(student_detail)
            try:
                Student.objects.bulk_create(student_base_list)
            except ObjectDoesNotExist as e:
                logger.error(e)
                result = False
                data = ""
                error = "批量插入学生失败"
                return JsonResponse({"result": result, "data": data, "error": error})
            for student_detail in student_detail_info:
                student_code = student_detail['student_code']
                name = student_detail['name']
                liaisons = student_detail['liaisons']
                liaisons_mobile = student_detail['liaisons_mobile']
                major_code = student_detail['major_code']
                major = student_detail['major']
                grade = student_detail['grade']
                class_info = student_detail['class_info']
                try:
                    student = Student.objects.filter(studentid=student_code, name=name)
                    major = Major.objects.filter(major_id=major_code, major_name=major)
                    grade = Grade.objects.filter(grade=grade)
                    class_info = ClassInfo.objects.filter(class_name=class_info)
                except ObjectDoesNotExist as e:
                    logger.warning(e)
                    result = False
                    data = ""
                    error = "格式不正确"
                    return JsonResponse({"result": result, "data": data, "error": error})
                student_detail_list.append(
                    StudentDetail(liaisons=liaisons, liaisons_mobile=liaisons_mobile, student_id=student[0].id,
                                  major_id=major[0].id,
                                  grade_id=grade[0].id, class_info_id=class_info[0].id))
            try:
                StudentDetail.objects.bulk_create(student_detail_list)
            except ObjectDoesNotExist as e:
                # Student.objects.extra(where=["studentid in students_codes"]).delete()
                logger.error(e)
                result = False
                data = ""
                error = "批量插入学生失败"
                return JsonResponse({"result": result, "data": data, "error": error})
        file_zip = zipfile.ZipFile(file_zip, 'r')
        save_path = os.getcwd()
        file_zip.extractall(save_path + "/media/")  # 解压缩
        for file in os.listdir(save_path + "/media/" + zip_name):
            image_type = file.split('.')[1]
            if image_type == "png" or image_type == "jpg" or image_type == "jpeg":
                image_name = file.split('.')[0]
                student = Student.objects.filter(studentid=image_name)
                if not student:
                    continue
                student.update(face=zip_name+"/"+image_name+"."+image_type)
        result = True
        data = "批量插入学生成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})



class ExportCollegeView(APIView):
    def post(self, request):
        college_code = request.POST.get("college_code", "")
        college_name = request.POST.get("college_name", "")
        if college_code == "" or college_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        college = College.objects.filter(college_id=college_code, college_name=college_name)
        if not college:
            result = False
            data = ""
            error = "院系参数有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        majors = Major.objects.filter(college_id=college[0].id)
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, label='学号')
        sheet.write(0, 1, label='姓名')
        sheet.write(0, 2, label='性别')
        sheet.write(0, 3, label='联系电话')
        sheet.write(0, 4, label='紧急联络人')
        sheet.write(0, 5, label='紧急联络人电话')
        sheet.write(0, 6, label='专业')
        sheet.write(0, 7, label='年级')
        sheet.write(0, 8, label='班级')
        for major in majors:
            student = StudentDetail.objects.filter(major=major)
            students_data = StudentDetailSerializer(student, many=True)
            students_data = students_data.data
            student_list = list()
            for data in students_data:
                student_list_a = list()
                student_code = data['student']['student_code']
                name = data['student']['name']
                sex = data['student']['sex']
                phone = data['student']['phone']
                liaisons = data['liaisons']
                liaisons_mobile = data['liaisons_mobile']
                major = data['major']
                grade = data['grade']
                class_info = data['class_info']
                student_list_a.append(student_code)
                student_list_a.append(name)
                student_list_a.append(sex)
                student_list_a.append(phone)
                student_list_a.append(liaisons)
                student_list_a.append(liaisons_mobile)
                student_list_a.append(major)
                student_list_a.append(grade)
                student_list_a.append(class_info)
                student_list.append(student_list_a)
            for row in range(0, len(student_list)):
                column = 0
                infos = student_list[row]
                for info in infos:
                    sheet.write(row+1, column, info)
                    column += 1
        # wbk.save('exportcollege' + '.xls')
        # wbk.save('exportcollege' + '.xls')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=exportcollege.xls'
        # output = io.StringIO()
        # wbk.save(output)
        # output.seek(0)
        # response.write(output.getvalue())
        return response
        # result = True
        # data = response
        # error = ""
        # return JsonResponse({"result": result, "data": data, "error": error})


class ExportGradeView(APIView):
    def post(self, request):
        grade = request.POST.get("grade", "")
        if grade == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        grade = Grade.objects.filter(grade=grade)
        if not grade:
            result = False
            data = ""
            error = "年级参数有误"
            return JsonResponse({"result": result, "data": data, "error": error})
        student = StudentDetail.objects.filter(grade_id=grade[0].id)
        students_data = StudentDetailSerializer(student, many=True)
        students_data = students_data.data
        student_list = list()
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, label='学号')
        sheet.write(0, 1, label='姓名')
        sheet.write(0, 2, label='性别')
        sheet.write(0, 3, label='联系电话')
        sheet.write(0, 4, label='紧急联络人')
        sheet.write(0, 5, label='紧急联络人电话')
        sheet.write(0, 6, label='专业')
        sheet.write(0, 7, label='年级')
        sheet.write(0, 8, label='班级')
        for data in students_data:
            student_list_a = list()
            student_code = data['student']['student_code']
            name = data['student']['name']
            sex = data['student']['sex']
            phone = data['student']['phone']
            liaisons = data['liaisons']
            liaisons_mobile = data['liaisons_mobile']
            major = data['major']
            grade = data['grade']
            class_info = data['class_info']
            student_list_a.append(student_code)
            student_list_a.append(name)
            student_list_a.append(sex)
            student_list_a.append(phone)
            student_list_a.append(liaisons)
            student_list_a.append(liaisons_mobile)
            student_list_a.append(major)
            student_list_a.append(grade)
            student_list_a.append(class_info)
            student_list.append(student_list_a)
        for row in range(0, len(student_list)):
            column = 0
            infos = student_list[row]
            for info in infos:
                sheet.write(row + 1, column, info)
                column += 1
        # wbk.save('exportgrade' + '.xls')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=exportcollege.xls'
        return response
        # output = io.StringIO()
        # wbk.save(output)
        # output.seek(0)
        # response.write(output.getvalue())
        # result = True
        # data = response
        # error = ""
        # return JsonResponse({"result": result, "data": data, "error": error})


class ExportSexView(APIView):
    def post(self, request):
        sex = request.POST.get("sex", "")
        if sex == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        if sex == u'男':
            sex = 0
        elif sex == u'女':
            sex = 1
        else:
            sex = sex
        students = Student.objects.filter(sex=sex)
        if not students:
            result = False
            data = ""
            error = "未查询到信息..."
            return JsonResponse({"result": result, "data": data, "error": error})
        wbk = xlwt.Workbook()
        sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
        sheet.write(0, 0, label='学号')
        sheet.write(0, 1, label='姓名')
        sheet.write(0, 2, label='性别')
        sheet.write(0, 3, label='联系电话')
        sheet.write(0, 4, label='紧急联络人')
        sheet.write(0, 5, label='紧急联络人电话')
        sheet.write(0, 6, label='专业')
        sheet.write(0, 7, label='年级')
        sheet.write(0, 8, label='班级')
        student_list = list()
        for student in students:
            student_list_a = list()
            student_detail = StudentDetail.objects.filter(student=student)
            student_data = StudentDetailSerializer(student_detail, many=True)
            student_data = student_data.data
            student_code = student_data[0]['student']['student_code']
            name = student_data[0]['student']['name']
            sex = student_data[0]['student']['sex']
            phone = student_data[0]['student']['phone']
            liaisons = student_data[0]['liaisons']
            liaisons_mobile = student_data[0]['liaisons_mobile']
            major = student_data[0]['major']
            grade = student_data[0]['grade']
            class_info = student_data[0]['class_info']
            student_list_a.append(student_code)
            student_list_a.append(name)
            student_list_a.append(sex)
            student_list_a.append(phone)
            student_list_a.append(liaisons)
            student_list_a.append(liaisons_mobile)
            student_list_a.append(major)
            student_list_a.append(grade)
            student_list_a.append(class_info)
            student_list.append(student_list_a)
        for row in range(0, len(student_list)):
            column = 0
            infos = student_list[row]
            for info in infos:
                sheet.write(row + 1, column, info)
                column += 1
        wbk.save('exportsex' + '.xls')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=exportcollege.xls'
        return response
        # output = io.StringIO()
        # wbk.save(output)
        # output.seek(0)
        # response.write(output.getvalue())
        # result = True
        # data = response
        # error = ""
        # return JsonResponse({"result": result, "data": data, "error": error})

# import os
# class Batch_Face(APIView):
#     def post(self, request):
#         file_zip = request.FILES.get("file_zip", "")
#         type_file = file_zip.name.split('.')[1]
#         file_name = file_zip.name.split('.')[0]
#         if type_file != "zip":
#             result = False
#             data = ""
#             error = "上传文件格式不是zip"
#             return JsonResponse({"result": result, "data": data, "error": error})
#         file_zip = zipfile.ZipFile(file_zip, 'r')
#         save_path = os.getcwd()
#         file_zip.extractall(save_path+"/media/")  # 解压缩
#         for file in os.listdir(save_path+"/media/"+file_name):
#             image_type = file.split('.')[1]
#             if image_type == "png" or image_type == "jpg" or image_type == "jpeg":
#                 image_name = file.split('.')[0]
#                 student = Student.objects.filter(studentid=image_name)
#                 if not student:
#                     continue
#                 student.update(face=file_name+"/"+image_name+"."+image_type)
#         result = True
#         data = ""
#         error = "ok"
#         return JsonResponse({"result": result, "data": data, "error": error})


class Finger_Collect(APIView):

    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        finger_picture = request.POST.get("finger_picture", "")
        if student_code == "" or student_name == "" or finger_picture == "":
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
            error = "学生信息不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        student.studentid = student_name
        student.name = student_name
        student.finger = finger_picture
        student.save()
        result = True
        data = "信息采集成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class Binding_Build(APIView):
    def get(self, request):
        build = request.POST.get("build", "")
        room = request.POST.get("room", "")
        if build =="" or room == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            room = DormRoom.objects.filter(build__buildname=build, room_id=room)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "未找到宿舍信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        roomsdata = BedNumberSerializer(room, many=True)
        result = True
        data = roomsdata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        build_id = request.POST.get("build_id", "")
        room_id = request.POST.get("room_id", "")
        bed_number = request.POST.get("bed_number", "")
        if student_code == "" or student_name == "" or build_id == "" or room_id == "" or bed_number == "":
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
            error = "学生信息不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            room = DormRoom.objects.get(build_id=build_id, room_id=room_id)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "宿舍信息不正确"
            return JsonResponse({"result": result, "data": data, "error": error})
        if room.isFull == True:
            result = False
            data = ""
            error = "该宿舍已满"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            BedNumber.objects.create(room=room, bed_num=bed_number, student=student)
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = ""
            error = "绑定宿舍失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "绑定宿舍成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        if student_code == "" or student_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        bed_info = BedNumber.objects.filter(student_code=student_code)
        if not bed_info:
            result = False
            data = ""
            error = "未找到该学生住宿信息"
            return JsonResponse({"result": result, "data": data, "error": error})
        bed_info.delete()
        result = True
        data = ""
        error = "退宿成功"
        return JsonResponse({"result": result, "data": data, "error": error})












