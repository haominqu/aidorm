from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import *
from college.models import Major
from django.core.exceptions import ObjectDoesNotExist
import logging
from .serializers import *


# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')


class StudentEdit(APIView):
    def get(self, request):
        studbid = request.POST.get('studbid', '')
        student = Student.objects.filter(id=studbid)
        result = True
        data = StudentListSerializer(student).data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def post(self, request):
        stuid = request.POST.get('stuid', '')
        name = request.POST.get('name', '')
        sex = request.POST.get('sex', '')
        phone = request.POST.get('phone', '')
        liaisons = request.POST.get('liaisons', '')
        mobile = request.POST.get('liaisons_mobile', '')
        major = request.POST.get('major', '')
        try:
            Student.objects.create(studentid=stuid, name=name, sex=sex, phone=phone)
            student = Student.objects.filter(studentid=stuid)
            major = Major.objects.filter(major_name=major)
            StudentDetail.objects.create(student_id=student[0].id, liaisons=liaisons, liaisons_mobile=mobile, major=major[0].id)
        except ObjectDoesNotExist as e:
            logger.error(e)
        result = True
        data = {'message': 'add success'}
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})

    def delete(self, request):
        result = True
        data = {}
        error = ""
        try:
            Student.objects.filter(isGraduate=True).delete()
            data = {'message': 'delete success'}
        except ObjectDoesNotExist as e:
            logger.error(e)
            result = False
            data = {}
            error = e
        return JsonResponse({"result": result, "data": data, "error": error})

    def patch(self, request):
        pass






