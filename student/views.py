from django.shortcuts import render
from rest_framework.views import APIView


# Create your views here.

class StudentInfo(APIView):
    def get(self, request):
        pass

    def post(self, request):
        face = request.POST.get('face', '')
        finger = request.POST.get('finger', '')
        pass

