from rest_framework import serializers
from .models import *

class CollegeSerializer(serializers.ModelSerializer):

    class Meta:
        model = College
        fields = ('id', 'college_id', 'college_name')


class MajorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Major
        fields = ('id', 'major_id', 'major_name', 'college')

    college = serializers.SerializerMethodField('college_field')
    def college_field(self, obj):
        return obj.college.college_name


class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id', 'grade')


