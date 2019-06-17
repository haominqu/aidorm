# restful API
from rest_framework.views import APIView

#django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.db import transaction
from django.shortcuts import HttpResponse

# selfproject
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

# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')

# student edit
class StudentEdit(APIView):

    def get(self, request):
        student_code = request.POST.get('student_code', '')
        student_name = request.POST.get('student_name', '')
        if student_code == "" or student_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.filter(studentid=student_code, name=student_name)
        except ObjectDoesNotExist as e:
            logger.error(e)
        student_detail = StudentDetail.objects.filter(student=student)
        studentdata = StudentDetailSerializer(student_detail, many=True)
        result = True
        data = studentdata.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        """add student base info"""
        student_code = request.POST.get('student_code', '')
        student_name = request.POST.get('student_name', '')
        gender = request.POST.get('gender', '')
        phone = request.POST.get('phone', '')
        liaisons = request.POST.get('liaisons', '')
        liaisons_mobile = request.POST.get('liaisons_mobile', '')
        major_code = request.POST.get('major_code', '')
        grade = request.POST.get('grade', '')
        if student_code=='' or student_name=='' or gender=='' or phone=='' or liaisons=='' or liaisons_mobile=='' or major_code=='' or grade=='':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            newstudent = Student.objects.create(studentid=student_code, name=student_name, sex=gender, phone=phone)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            result = False
            data = ""
            error = "添加学生失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            major = Major.objects.filter(major_code=major_code)
            grade = Grade.objects.filter(grade=grade)
            StudentDetail.objects.create(liaisons=liaisons, liaisons_mobile=liaisons_mobile, student=newstudent, major=major, grade=grade)
        except ObjectDoesNotExist as e:
            logging.warning(e)
            newstudent.delete()
            result = False
            data = ""
            error = "添加学生失败"
            return JsonResponse({"result": result, "data": data, "error": error})
        result = True
        data = "添加学生成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        student_code = request.POST.get('student_code', '')
        student_name = request.POST.get('student_name', '')
        if student_code == "" or student_name == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            student = Student.objects.filter(studentid=student_code, name=student_name)
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
        student_code = request.POST.get('student_code', '')
        student_name = request.POST.get('student_name', '')
        new_mobile = request.POST.get('new_mobile', '')
        if student_code == "" or student_name == "" or new_mobile == "":
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        student = Student.objects.filter(studentid=student_code, name=student_name)
        if not student:
            result = False
            data = ""
            error = "请输入正确学号姓名"
            return JsonResponse({"result": result, "data": data, "error": error})
        student.update(phone=new_mobile)
        result = True
        data = ""
        error = "修改成功"
        return JsonResponse({"result": result, "data": data, "error": error})


class BatchCreateView(APIView):
    def post(self, request):
        f = request.FILES['my_file']
        type_excel = f.name.split('.')[1]
        if 'xls' == type_excel:
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
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
                    student_detail['grade'] = str(int(rowValues[8]))
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
                    try:
                        student = Student.objects.filter(studentid=student_code, name=name)
                        major = Major.objects.filter(major_id=major_code, major_name=major)
                        grade = Grade.objects.filter(grade=grade)
                    except ObjectDoesNotExist as e:
                        logger.warning(e)
                        result = False
                        data = ""
                        error = "格式不正确"
                        return JsonResponse({"result": result, "data": data, "error": error})
                    student_detail_list.append(
                        StudentDetail(liaisons=liaisons, liaisons_mobile=liaisons_mobile, student_id=student[0].id,
                                      major_id=major[0].id,
                                      grade_id=grade[0].id))
                try:
                    StudentDetail.objects.bulk_create(student_detail_list)
                except ObjectDoesNotExist as e:
                    # Student.objects.extra(where=["studentid in students_codes"]).delete()
                    logger.error(e)
                    result = False
                    data = ""
                    error = "批量插入学生失败"
                    return JsonResponse({"result": result, "data": data, "error": error})
                result = True
                data = "批量插入学生成功"
                error = ""
                return JsonResponse({"result": result, "data": data, "error": error})
        result = False
        data = ""
        error = "上传文件格式不是xls"
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
                student_list_a.append(student_code)
                student_list_a.append(name)
                student_list_a.append(sex)
                student_list_a.append(phone)
                student_list_a.append(liaisons)
                student_list_a.append(liaisons_mobile)
                student_list_a.append(major)
                student_list_a.append(grade)
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
            student_list_a.append(student_code)
            student_list_a.append(name)
            student_list_a.append(sex)
            student_list_a.append(phone)
            student_list_a.append(liaisons)
            student_list_a.append(liaisons_mobile)
            student_list_a.append(major)
            student_list_a.append(grade)
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
            student_list_a.append(student_code)
            student_list_a.append(name)
            student_list_a.append(sex)
            student_list_a.append(phone)
            student_list_a.append(liaisons)
            student_list_a.append(liaisons_mobile)
            student_list_a.append(major)
            student_list_a.append(grade)
            student_list.append(student_list_a)
        for row in range(0, len(student_list)):
            column = 0
            infos = student_list[row]
            for info in infos:
                sheet.write(row + 1, column, info)
                column += 1
        # wbk.save('exportsex' + '.xls')
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


class Face_Collect(APIView):

    def post(self, request):
        student_code = request.POST.get("student_code", "")
        student_name = request.POST.get("student_name", "")
        face_picture = request.POST.get("face_picture", "")
        if student_code == "" or student_name == "" or face_picture == "":
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
        student.face = face_picture
        student.save()
        result = True
        data = "信息采集成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


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












