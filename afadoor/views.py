from django.shortcuts import render
from django.http import JsonResponse,request
from django.core.exceptions import ObjectDoesNotExist

from dormitory.models import FaceMachine, BedNumber, Student
from .serializers import *

from rest_framework.views import APIView

import logging
# Create your views here.

logger = logging.getLogger('sourceDns.webdns.views')

class GetFaceList(APIView):

    def get(self, request):
        machine_id = request.GET.get('machine_no')
        ip = request.META['REMOTE_ADDR']
        print()
        try:
            machine=FaceMachine.objects.get(machine_no=machine_id)
        except ObjectDoesNotExist as e:
            logger.error(e)
        if machine.machine_status is 1 and machine.machine_ip == ip:
            build_id = machine.build
            student_list = Student.objects.filter(stu__room__build_id=build_id)
            students_list = StudrentListSerializer(student_list, many=True)

            print("@@@",students_list.data)

        result = True
        data = students_list.data
        error = ""
        return JsonResponse({"result": result, "data": data, "error": error})


