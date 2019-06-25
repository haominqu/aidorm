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
        return obj.get_college()



class GradeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Grade
        fields = ('id', 'grade')


class GlassSerializer(serializers.ModelSerializer):
    college = serializers.SerializerMethodField('college_field')
    def college_field(self, obj):
        return obj.major.college.college_name

    major = serializers.SerializerMethodField('major_field')
    def major_field(self, obj):
        return obj.major.major_name

    grade = serializers.SerializerMethodField('grade_field')
    def grade_field(self, obj):
        return obj.grade.grade

    guide = serializers.SerializerMethodField('guide_field')
    def guide_field(self, obj):
        return obj.guide.username

    is_graduation = serializers.SerializerMethodField('is_graduation_field')
    def is_graduation_field(self, obj):
        return obj.get_gradution()

    class Meta:
        model = ClassInfo
        fields = ('id', 'college', 'major', 'grade', 'class_name', 'guide', 'is_graduation')