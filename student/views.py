# restful API
from rest_framework.views import APIView

#django
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse

# selfproject
from .serializers import *
from .models import *
from college.models import Major
from dormitory.models import *

# base
import logging

# Create your views here.

# logger = logging.getLogger('sourceDns.webdns.views')

# student edit
class StudentEdit(APIView):

    def get(self, request):
        studbid = request.POST.get('studbid', '')
        result = True
        data = ""
        error = ""
        if studbid == "":
            result = False
            error = "id不能为空"
        else:
            student = Student.objects.filter(id=studbid)
            studentdata = StudentSerializer(student, many=True)
            data = studentdata.data
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        """add student base info"""
        stuid = request.POST.get('stuid', '')
        name = request.POST.get('name', '')
        sex = request.POST.get('sex', '')
        phone = request.POST.get('phone', '')
        if stuid=='' or name=='' or sex=='' or phone=='':
            result = False
            data = ""
            error = "信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            Student.objects.create(studentid=stuid, name=name, sex=sex, phone=phone)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        result = True
        data = "添加成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        pass

    def patch(self, request):
        studbid = request.POST.get('studbid', '')
        liaisons = request.POST.get('liaisons', '')
        liamobile = request.POST.get('liamobile', '')
        if studbid == "" or liaisons == "" or liamobile == "":
            result = False
            data = ""
            error = "id,信息不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            stu = StudentDetail.objects.get(student_id=studbid)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        stu.liaisons = liaisons
        stu.liaisons_mobile = liamobile
        stu.save()
        result = True
        data = "修改成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


class StuDetailEdit(APIView):
    def get(self, request):
        pass

    def post(self, request):
        pass

    def delete(self, request):
        pass

    def patch(self, request):
        studbid = request.POST.get('studbid', '')
        roomno = request.POST.get('roomno', '')
        if studbid == "" or roomno == "":
            result = False
            data = ""
            error = "id,房间号不能为空"
            return JsonResponse({"result": result, "data": data, "error": error})
        try:
            stu = StudentDetail.objects.get(student_id=studbid)
            room = DormRoom.objects.get(room_id=roomno)
        except ObjectDoesNotExist as e:
            logging.warning(e)
        stu.dormitory = room
        stu.save()
        result = True
        data = "绑定宿舍成功"
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})








