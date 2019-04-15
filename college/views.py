from django.shortcuts import render
# restful API
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework import permissions

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
        pass

    def post(self, request):

        pass

    def delete(self, request):
        pass

    def patch(self, request):
        pass